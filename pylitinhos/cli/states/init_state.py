import sys
import Pyro4
from colorama import Fore
from pylitinhos.remote.model import *
from ..color import *
from ..smlite import State
from getpass import getpass


class InitState(State):

    def run(self, arguments={}):
        print()
        print(text_default("Pylitinhos"))
        print(text_default("Um jogo de adivinhação e aposta"))
        print()
        print(text_primary("> Setup < "))
        print(text_default("Conexão com o servidor... "), end="")
        try:
            self.player.proxy = self.create_rmi_proxy()
            print(text_success("OK", prefix=""))
        except Exception:
            text_danger("ERRO")
            text_danger("Verifique se o servidor está online "
                        "e tente novamente")
            exit()

        print()
        text_info("## Identificação ##")

        self.player.name, self.player.room_name = self.register_player(
            self.player.proxy
        )

        return False

    def create_rmi_proxy(self):
        Pyro4.config.SERIALIZER = 'pickle'
        return Pyro4.Proxy("PYRONAME:gameserver.pyro")

    def register_player(self, proxy):
        registered = False
        name = None
        room_name = None

        print(text_primary("> Identificação < "))
        while not registered:
            print()
            username = input(text_default("Username: "))
            password = getpass(text_default("Password: "))

            response = proxy.authenticate_user(username, password)
            if response.is_ok():
                registered = True
            else:
                if response.get_cause == Error.Causes.PlayerAlreadyOnRoom:
                    print(text_danger(
                        "Nome de usuário inválido! Escolha outro."))
                elif response.get_cause == Error.Causes.InvalidLogin:
                    print(text_danger(
                        "Informações de login incorretas. Tente novamente."))
                elif response.get_cause == Error.Causes.NewUser:
                    d = input(text_info("Usuário %s ainda não foi utilizado."
                                        "Deseja criar um novo usuário? (s/n)"))

                    if d.lower() == 's':
                        registered = self.register_new_player(username,
                                                              password,
                                                              proxy)
                else:
                    print(text_danger("Error: "), response.error_msg())

        return (name, room_name)

    def register_new_player(self, username, password, proxy):
        okay = False
        print(text_primary("> Novo Usuário < "))
        while not okay:
            print()
            nickname = input(text_default("Apelido: "))
            # repass = getpass(text_default("Repita a senha: "))

            print()
            print(text_info("Confirme suas informações"))
            print(text_default("Apelido: %s" % nickname))
            print(text_default("Username: %s" % username))
            print()
            r = input(text_info("As informações estão corretas? (s/n)"))

            if r.lower() == 's':
                response = proxy.register_new_player(username, password,
                                                     nickname)
                okay = True

        return True

    def enter_room():
        print(text_primary("> Sala de jogo < "))
        room_name = input(text_default("Nome da sala: "))

        response = proxy.registerPlayer(name, room_name)

        if response.is_ok():
            registered = True
        else:
            if response.get_cause == Error.Causes.PlayerAlreadyOnRoom:
                print("Nome de usuário inválido! Escolha outro.")
            else:
                print("Error: ", response.error_msg())
