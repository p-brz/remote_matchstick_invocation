from .model import *
from ..db.Data import Data
from ..db.UserDAO import UserDAO
from pylitinhos.model.Event import *

from sqlalchemy.orm.exc import NoResultFound

from concurrent.futures import ThreadPoolExecutor
import threading


class GameManager(object):

    def __init__(self, **kw):
        self.db = kw.get('db', None)
        if self.db is None:
            self.db = Data()

        self.room_observers = {}
        self.room_infos = {}
        self.executor = ThreadPoolExecutor(max_workers=2)

        #Usa isto para testes (evita uso de operações asincronas)
        self.synchronous = False

    def echo(self):
        return True

    def destroy(self):
        self.executor.shutdown()
        self.db.destroy()

    def authenticate_user(self, username, password):
        user_authenticated = self.db.users.verify(username, password)
        if user_authenticated:
            return Response()
        else:
            if self.db.users.exist(username):
                return Response(error=Error(Error.Causes.InvalidLogin))
            else:
                return Response(error=Error(Error.Causes.NewUser))

    def register_new_player(self, username, password, nickname):
        '''Cria um novo usuário'''
        try:
            self.db.users.create(username, password, nickname=nickname)
            return Response()
        except:
            return Response(error=Error(Error.Causes.CreationError))

    def get_room(self, room_name):
        return Response(bundle=Bundle(room=self.db.rooms.get(room_name).clone()))

    def get_match_info(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        names = room.get_players_names()
        infos = {}
        for name in names:
            player = room.get_player(name=name)
            infos.update({name: player.palitos})
        return Response(bundle=Bundle(match=infos))

    def set_ready(self, room_name, player_name):
        room = self.db.rooms.get(room_name).clone()
        player = room.get_player(name=player_name)

        player.ready = True
        self.db.players.save(player)
        self.check_all_ready(room_name)

    def check_all_ready(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        names = room.get_players_names()
        all_ready = True
        for name in names:
            player = room.get_player(name=name)
            if not player.ready:
                all_ready = False
                break

        if all_ready:
            self.setup_game(room_name)


    def setup_game(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        self.room_infos.update({
            room_name: {
                'current_round': 1,
                'order': room.get_players_names(),
                'bets': {},
                'guesses': {}
            }
        })

        evt = Event(EventTypes.StartRound,
                    player_name=self.room_infos[room_name]['order'][0],
                    round=self.room_infos[room_name]['current_round'])
        self._notify_room_event(room_name, evt)


    def room_exist(self, room_name):
        exist = self.db.rooms.exist(room_name)
        return Response(bundle=Bundle(exist=exist))

    def add_player_to_room(self, player_name, room_name):

        player = None
        try:
            # Cria sala e player (se ja não tiverem sido criados)
            player = self.db.rooms.add_player(room_name, player_name)
        except NoResultFound:
            return Response(error=Error(Error.Causes.InexistentUser))

        evt = Event(EventTypes.AddedUser, player_name=player_name, room_name=room_name)
        self._notify_room_event(room_name, evt)

        return Response(bundle=Bundle(player=player))

    def can_start_game(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        return room.player_count() >= 2

    def start_game(self, room_name):
        print("Starting game")
        evt = Event(EventTypes.NewGame, valid=True)

        print("Start game evt:", evt)

        self._notify_room_event(room_name, evt)

    def make_bet(self, room_name, player_name, bet):
        current_round = self.room_infos[room_name]['current_round']
        bet = int(bet)
        if current_round == 1 and bet == 0:
            print("First Null")
            return Response(error=Error(Error.Causes.FirstBetNull))

        room = self.db.rooms.get(room_name).clone()
        player = room.get_player(name=player_name)

        if bet > player.palitos or bet < 0:
            print("Invalid")
            return Response(error=Error(Error.Causes.InvalidBet))

        self.room_infos[room_name]['bets'].update({
            player_name: bet
        })

        return Response()


    def end_betting_turn(self, room_name, player_name):
        index = 0
        for name in self.room_infos[room_name]['order']:
            if name == player_name:
                break
            else:
                index = index + 1

        if index == (len(self.room_infos[room_name]['order']) - 1):
            evt = Event(EventTypes.StartGuessing,
                        player_name=self.room_infos[room_name]['order'][0])
        else:
            next_player = self.room_infos[room_name]['order'][index + 1]
            evt = Event(EventTypes.ChangeChoiceTurn,
                        player_name=next_player)

        self._notify_room_event(room_name, evt)

    def make_guess(self, room_name, player_name, guess):
        room = self.db.rooms.get(room_name).clone()
        guess = int(guess)
        sum_palitos = 0
        for pname in room.players:
            sum_palitos += room.get_player(name=pname).palitos

        if guess <= 0 or guess > sum_palitos:
            return Response(error=Error(Error.Causes.InvalidGuess))

        self.room_infos[room_name]['guesses'].update({
            player_name: guess
        })

        evt = Event(EventTypes.OnPlayerGuess,
                    player_name=player_name,
                    room_name=room_name,
                    guess=guess)

        self._notify_room_event(room_name, evt)

        return Response()

    def end_guessing_turn(self, room_name, player_name):
        index = 0
        for name in self.room_infos[room_name]['order']:
            if name == player_name:
                break
            else:
                index = index + 1

        if index == (len(self.room_infos[room_name]['order']) - 1):
            self.launch_result(room_name)
        else:
            next_player = self.room_infos[room_name]['order'][index + 1]
            evt = Event(EventTypes.ChangeGuessingTurn,
                        player_name=next_player)
            self._notify_room_event(room_name, evt)

    def launch_result(self, room_name):
        total_bet = 0
        winner = None
        for player, bet in self.room_infos[room_name]['bets'].items():
            total_bet = total_bet + int(bet)

        for player, guess in self.room_infos[room_name]['guesses'].items():
            if guess == total_bet:
                winner = player
                break

        evt = Event(EventTypes.FinishRound,
                    bets=self.room_infos[room_name]['bets'],
                    total=total_bet,
                    winner=winner)

        first = self.room_infos[room_name]['order'].pop(0)
        self.room_infos[room_name]['order'].append(first)
        self.room_infos[room_name]['current_round'] += 1

        room = self.db.rooms.get(room_name).clone()

        self._notify_room_event(room_name, evt)
        if winner is not None:
            player = room.get_player(name=winner)
            player.palitos -= 1

            self.db.players.save(player)

            if player.palitos == 0:
                index = 0
                for name in self.room_infos[room_name]['order']:
                    if name == winner:
                        break
                    else:
                        index = index + 1

                self.room_infos[room_name]['order'].pop(index)
                win_evt = Event(EventTypes.OnPlayerWin,
                                player_name=winner)
                self._notify_room_event(room_name, win_evt)

        players = self.room_infos[room_name]['order']
        if len(players) == 1:
            st_evt = Event(EventTypes.MatchFinished,
                           player_name=self.room_infos[room_name]['order'][0])
            self._notify_room_event(room_name, st_evt)
        else:
            st_evt = Event(EventTypes.StartRound,
                           player_name=self.room_infos[room_name]['order'][0],
                           round=self.room_infos[room_name]['current_round'])
            self._notify_room_event(room_name, st_evt)


    def observe_room(self, room_name, observer):
        if not observer:
            return Response(error=Error(Error.Causes.NoObserver))

        if room_name not in self.room_observers:
            self.room_observers[room_name] = []

        self.room_observers[room_name].append(observer)

        return Response()

    def _notify_room_event(self, room_name, evt):
        def notify_room_event_async(self, evt, observers):
            if observers:
                print("notify evt async : ", evt, " for %d observers" % len(observers))
                for observer in observers:
                    observer.on_event(evt)

        observers = self.room_observers.get(room_name, None)

        if observers:
            if not self.synchronous:
                self.executor.submit(notify_room_event_async, self, evt, observers)
            else:
                notify_room_event_async(self, evt, observers)
