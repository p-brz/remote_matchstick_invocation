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
        self.evLoop = kw.get('event_loop', None)
        super(GameState, self).__init__(player)

    def run(self, arguments={}):
        self.evLoop = arguments.get('event_loop', self.evLoop)

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

        if self.i_am_winner():
            print(text_success("A conta não é sua hoje"))
        else:
            print(text_danger("Parece que hoje você paga a conta"))

        return False

    def event_loop(self):
        for evt in self.evLoop.events():
            self.on_event(evt)

    def on_event(self, evt):
        callback = {
            EventTypes.StartRound          : self.on_start_round,
            EventTypes.ChangeChoiceTurn    : self.on_change_choice_turn,
            EventTypes.ChangeGuessingTurn  : self.on_change_guessing_turn,
            EventTypes.OnPlayerGuess       : self.on_player_guess,
            EventTypes.FinishRound         : self.on_finish_round,
            EventTypes.OnPlayerWin         : self.on_player_win,
            EventTypes.MatchFinished       : self.on_match_finish
        }.get(evt.type, None)

        if callback:
            self.callback(evt)

    def on_start_round(self, evt):
        '''Começa rodada'''
        pass

    def on_change_choice_turn(self, evt):
        ''' Muda a rodada de quem deve escolher os palitos'''

        #TODO: verificar se é a rodada deste jogador
        pass

    def on_change_guessing_turn(self, evt):
        '''Vez de alguém fazer uma aposta
            evento deve conter apostas ja feitas
        '''
        #TODO: verificar se é a rodada deste jogador
        pass

    def on_player_guess(self, evt):
        '''Algum jogador fez sua aposta'''
        #NOTE: pode ser que seja o próprio jogador
        pass

    def on_finish_round(self, evt):
        '''Finalizou a rodada, evento deve conter o resultado e quem acertou
            -se alguem tiver acertado-
        '''
        pass

    def on_player_win(self, evt):
        '''Algum jogador venceu o jogo - está sem palitos'''
        pass

    def on_match_finish(self, evt):
        '''Fim da partida.'''
        pass

    def show_match_infos(self):
        print(text_primary("Quantidade de palitos no jogo"))
        response = self.player.proxy.get_match_info(self.player.room_name)
        palitinhos_info = response.bundle.get_data('match')
        print(palitinhos_info)
        for nick, palitinhos in palitinhos_info.items():
            print(text_info(nick + ": "), end='')
            print(text_default(palitinhos))

    def betting_phase(self):
        print()
        print(text_primary("1 - Aposta"))
        if not self.player.my_turn:
            print(text_info("Aguardando sua vez de jogar..."))
        while not self.player.my_turn:
            continue

        print()
        print(text_success("Sua vez"))
        bet_ok = False
        while not bet_ok:
            bet = input(text_primary("Informe a quantidade de palitos: "))
            bet_ok = self.check_valid_bet(bet)

        self.end_remote_turn()
        self.player.my_turn = False

    def guessing_phase(self):
        print()
        print(text_primary("2 - Palpite"))
        while not self.is_guess_phase():
            continue

        if not self.player.my_turn:
            print(text_info("Aguardando sua vez de jogar..."))
        while not self.player.my_turn:
            continue

        print(text_success("Sua vez"))
        guess_ok = False
        while not guess_ok:
            guess = input(text_primary("Informe um palpite: "))
            guess_ok = self.check_valid_guess(guess)

        self.end_remote_turn()
        self.player.my_turn = False

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
                print(text_danger("O primeira aposta não pode ser zero. "
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
