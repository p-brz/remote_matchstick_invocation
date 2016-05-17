from pylitinhos.cli import Client

import Pyro4

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = 'pickle'

def main():
    client = Client()
    client.start()
    print()

if __name__ == "__main__":
    main()
