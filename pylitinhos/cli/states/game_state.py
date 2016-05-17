import sys
import Pyro4
import Pyro4.util
from colorama import Fore
from pylitinhos.remote.model import *
from ..color import *
from ..smlite import State
from getpass import getpass

from pylitinhos.model.Event import *


class GameState(State):

    def __init__(self, player, **kw):
        super(GameState, self).__init__(player)

        self.evLoop = kw.get('event_loop', None)
        self.observer_thread = kw.get('observer_thread', None)
        self.keep_going = True

    def run(self, arguments={}):
        self.player.proxy.set_ready(
            self.player.room_name, self.player.name
        )
        self.evLoop = arguments.get('event_loop', self.evLoop)
        self.observer_thread = arguments.get('observer_thread', self.observer_thread)

        try:
            print(text_primary("> Início do jogo <"))

            # match_over = False
            # while not match_over:
            #     self.show_match_infos()
            #     self.betting_phase()
            #     self.guessing_phase()
            #     self.result_phase()
            #
            #     match_over = self.is_match_over_for_me()

            self.event_loop()
        finally:
            if self.observer_thread is not None:
                self.observer_thread.stop()

        return False

    def event_loop(self):
        for evt in self.evLoop.events():
            self.on_event(evt)
            if not self.keep_going:
                break

    def on_event(self, evt):
        callback = {
            EventTypes.StartRound          : self.on_start_round,
            EventTypes.ChangeChoiceTurn    : self.on_change_choice_turn,
            EventTypes.ChangeGuessingTurn  : self.on_change_guessing_turn,
            EventTypes.OnPlayerGuess       : self.on_player_guess,
            EventTypes.FinishRound         : self.on_finish_round,
            EventTypes.OnPlayerWin         : self.on_player_win,
            EventTypes.MatchFinished       : self.on_match_finish,
            EventTypes.StartGuessing       : self.on_start_guessing
        }.get(evt.type, None)

        if callback:
            callback(evt)

    def on_start_round(self, evt):
        '''Começa rodada'''
        print(text_primary("Rodada %d" % evt.data.get('round')))
        self.show_match_infos()

        print(text_primary("Etapa 1 - Aposta"))
        print()
        current_player = evt.data.get('player_name')
        if current_player == self.player.name:
            self.betting_phase()
        else:
            print(text_info("Vez do jogador "), end='')
            print(current_player)

    def on_change_choice_turn(self, evt):
        ''' Muda a rodada de quem deve escolher os palitos'''
        current_player = evt.data.get('player_name')
        if current_player == self.player.name:
            self.betting_phase()
        else:
            print(text_info("Vez do jogador "), end='')
            print(current_player)

    def on_start_guessing(self, evt):
        print(text_primary("Etapa 2 - Palpite"))
        print()
        current_player = evt.data.get('player_name')
        if current_player == self.player.name:
            self.guessing_phase()
        else:
            print(text_info("Vez do jogador "), end='')
            print(current_player)

    def on_change_guessing_turn(self, evt):
        '''Vez de alguém fazer uma aposta
            evento deve conter apostas ja feitas
        '''
        current_player = evt.data.get('player_name')
        if current_player == self.player.name:
            self.guessing_phase()
        else:
            print(text_info("Vez do jogador "), end='')
            print(current_player)

    def on_player_guess(self, evt):
        player = evt.data.get('player_name')
        guess = evt.data.get('guess')

        if player != self.player.name:
            print(text_info("O jogador %s deu como "
                            "palpite %d palito(s)" % (player, int(guess))))

    def on_finish_round(self, evt):
        print(text_primary("Fim da rodada"))
        print()
        print(text_info("Resultados:"))
        for player, bet in evt.data.get('bets').items():
            print("O jogador %s apostou %d palito(s)" % (player, bet))

        print()
        print(text_info("Total: "), end="")
        print(text_success(evt.data.get('total')))

        print()
        winner = evt.data.get('winner')
        if winner is None:
            print(text_warning("Não houveram vencedores nessa rodada"))
        else:
            if winner == self.player.name:
                print(text_success("Você venceu esta rodada"))
            else:
                print(text_warning("O jogador %s venceu esta rodada" % winner))

    def on_player_win(self, evt):
        winner = evt.data.get('player_name')
        if winner == self.player.name:
            print(text_success("Você venceu! A conta não é sua!"))
            self.keep_going = False
        else:
            print(text_success("Jogador %s está sem palitos e não "
                               "pagará a conta" % winner))

    def on_match_finish(self, evt):
        loser = evt.data.get('player_name')
        print(text_warning("Parece que o jogador %s terá que "
                           "pagar a conta" % loser))
        self.keep_going = False

    def show_match_infos(self):
        print(text_primary("Quantidade de palitos no jogo"))
        response = self.player.proxy.get_match_info(self.player.room_name)
        palitinhos_info = response.bundle.get_data('match')
        for nick, palitinhos in palitinhos_info.items():
            print(text_info(nick + ": "), end='')
            print(text_default(palitinhos))

    def betting_phase(self):
        print(text_success("É a sua vez"))
        bet_ok = False
        while not bet_ok:
            bet = input(text_primary("Informe a quantidade de palitos: "))
            bet_ok = self.check_valid_bet(bet)

        self.player.proxy.end_betting_turn(
            self.player.room_name,
            self.player.name
        )

    def guessing_phase(self):
        print(text_success("É a sua vez"))
        guess_ok = False
        while not guess_ok:
            guess = input(text_primary("Informe um palpite: "))
            guess_ok = self.check_valid_guess(guess)

        self.player.proxy.end_guessing_turn(
            self.player.room_name,
            self.player.name
        )

    def result_phase(self):
        print()
        print(text_primary("3 - Resultado"))
        while not self.is_result_phase():
            continue

        t_info = self.player.proxy.get_turn_result(self.player.room_name)
        total = t_info['total']
        if t_info['draw']:
            print(text_info("Nenhum jogador acertou a quantidade "
                            "de palitos (%d)" % total))
        elif t_info['name'] == self.player.name:
            print(text_success("Você venceu está rodada!"))
        else:
            w_guess = t_info['guess']
            w_nick = t_info['nick']
            print(text_warning("O jogador %s acertou a quantidade "
                               "de palitos (%d) e venceu a "
                               "rodada" % (w_nick, w_guess)))

    def check_valid_bet(self, bet):
        if not self.string_is_int(bet):
            print(text_danger("A aposta deve ser um número natural"))
            return False

        response = self.player.proxy.make_bet(self.player.room_name,
                                              self.player.name,
                                              bet)
        if response.is_ok():
            return True
        else:
            if response.cause == Error.Causes.InvalidBet:
                print(text_danger("Aposta inválida. "
                                  "Tente novamente"))
            elif response.cause == Error.Causes.FirstBetNull:
                print(text_danger("A primeira aposta não pode ser zero. "
                                  "Informe outro valor"))

            return False

    def check_valid_guess(self, guess):
        if not self.string_is_int(guess):
            print(text_danger("O palpite deve ser um número natural"))
            return False

        response = self.player.proxy.make_guess(self.player.room_name,
                                                self.player.name,
                                                guess)
        if response.is_ok():
            return True
        else:
            if response.cause == Error.Causes.InvalidGuess:
                print(text_danger("Palpite inválido. "
                                  "Tente novamente"))

            return False

    def string_is_int(self, strval):
        try:
            int(strval)
            return True
        except ValueError:
            return False

    def is_match_over_for_me(self):
        # TODO: Corrigir com chamada ao servidor
        return True

    def i_am_winner(self):
        # TODO: Corrigir com chamada ao servidor
        return True

    def is_guess_phase(self):
        # TODO: Corrigir com chamada ao servidor
        return True

    def is_bet_phase(self):
        # TODO: Corrigir com chamada ao servidor
        return True

    def end_guess_turn(self):
        self.player.proxy.end_guess_turn(self.player.room_name,
                                         self.player.name)

    def end_bet_turn(self):
        self.player.proxy.end_bet_turn(self.player.room_name,
                                       self.player.name)
        return
