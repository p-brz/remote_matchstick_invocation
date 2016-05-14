# (nome a definir)

## Instalação

### Python for android

Ver a [documentação deles](http://python-for-android.readthedocs.io/en/latest/quickstart/#installation)
para as dependências necessárias e instruções mais detalhadas.

    pip install git+https://github.com/kivy/python-for-android.git

### Kivy

Instruções de instação: https://kivy.org/docs/installation/installation.html


## Execução

Para executar o programa em ambiente desktop basta executar:

    python main.py

### Android


#### Configuração python-for-android

Antes de poder rodar o projeto em um dispositivo Android é preciso compilá-lo.

Para tanto é preciso ter a SDK e NDK Android instaladas e configuradas.

A documentação do [python-for-android](http://python-for-android.readthedocs.io/en/latest/quickstart/#setting-paths-to-the-the-sdk-and-ndk)
descreve como configurar o ambiente para que o **p4a** detecte a SDK.
Mas, em linhas gerais, é preciso definir as seguintes variáveis de ambiente:

    $export ANDROID_HOME=/caminho/para/a/sdk/do/android

    $export ANDROID_NDK_HOME=/caminho/para/a/ndk/android

#### Compilar apk

Por fim, basta executar o comando (na pasta raiz do projeto):

    p4a apk

e será gerado um arquivo **.apk** do projeto.

Pode ser preciso modificar a api alvo (caso você não tenha ela instalada) ou
outras configurações. Para isto modifique o arquivo **.p4a** (verifique a
documentação para identificar as opções válidas).

#### Instalar apk

Para instalar o apk em um dispositivo ou emulador, execute:

    adb install -r <caminho para o apk>

A opção '-r' permite substituir a aplicação caso ela ja esteja instalada.
