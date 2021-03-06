# Setting up Yandex.SpeechKit ASR

Download Python client library:

    git clone https://github.com/yandex/speechkitcloud

Add `protoc` to `PATH` by modifying `~/.bash_profile`:

    PATH="/Users/kirill/protoc-3.1.0-osx-x86_64/bin:${PATH}"
    export PATH

Precompiled `protoc` binaries can be found at <https://github.com/google/protobuf>.

To compile `*.proto` files into Python classes, use the following command:

```shell
protoc --proto_path=input_dir --python_out=output_dir input_dir/*.proto
```

## Notes

Available recognition models:
* `freeform` (default)
* `freeform8alaw` (use if your sound comes from a phone call) [Gives 500 Server Error]
* `general` (missing from the official API) [looks like it's the same as freeform]
* `notes` (missing from the official API)
* `queries`
* Other: `maps`, `dates`, `names`, `numbers`, `music`, `buying`

Use this host: `voice-stream.voicetech.yandex.net` and this port: 443 (SSL).





# Working with Python virtual environments

On Python 2.7:

```shell
sudo pip install virtualenv
virtualenv -p /usr/bin/python venv
source venv/bin/activate
pip install protobuf
pip freeze
deactivate
```

On Python 3.5:

```shell
python3 -m venv venv
source venv/bin/activate
pip3 install protobuf
pip3 freeze
deactivate
```

# Working with core part

compiled app take json input file as an argument. Result shoult be appear in the same folder and name with "out" suffix.



# Что делать

* Установить Python 3.5 или выше. Автоматически будет установлен pip.
* Добавить команды `python` и `pip` в переменную окружения `PATH` и убедиться, что они вызывают правильные версии этих программ.
Должен быть именно `python >= 3.5.*`, а pip должен устанавливать пакеты именно для этого Питона.
* Выполнить команду `pip install webrtcvad numpy` (возможно, с правами Администратора).
* Выполнить команду `python -c "import webrtcvad, numpy"` (убедиться, что всё установилось).
* Выполнить скрипт: `python dialog.py` и посмотреть на его stdout.
* Изучить этот скрипт (`dialog.py`). Вся работа с диалогом и дорожками в нём.
* Не нарушая существующего API, добавить вычисление оставшихся метрик по речи и перебиваниям (см. ниже). Делать можно в любом порядке.
Желательно получить элегантную реализацию на основе масок (см. класс `Mask`), что позволит все параметры вычислить общим способом.
* По возможности, необходимо комментировать код. На русском или английском языке.
