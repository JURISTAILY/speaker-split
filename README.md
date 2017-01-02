# Setting up Yandex.SpeechKit ASR

Add `protoc` to `PATH` by modifying `~/.bash_profile`:

    PATH="/Users/kirill/protoc-3.1.0-osx-x86_64/bin:${PATH}"
    export PATH

Precompiled `protoc` binaries can be found at <https://github.com/google/protobuf>.

To compile `*.proto` files into Python classes, use the following command:

```shell
protoc --proto_path=input_dir --python_out=output_dir input_dir/*.proto
```

## Working with Python virtual environments

On Python 2.7:

```bash
sudo pip install virtualenv
virtualenv -p /usr/src/python2.7 venv
source venv/bin/activate
pip install protobuf
pip freeze
deactivate
```

On Python 3.5:

```python
python3 -m venv venv
source venv/bin/activate
pip3 install protobuf
pip3 freeze
deactivate
```
