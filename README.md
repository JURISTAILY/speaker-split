# Setting up Yandex.SpeechKit ASR

Add `protoc` to `PATH` by modifying `~/.bash_profile`:

    PATH="/Users/kirill/protoc-3.1.0-osx-x86_64/bin:${PATH}"
    export PATH

Precompiled `protoc` binaries can be found at <https://github.com/google/protobuf>.

To compile `*.proto` files into Python classes, use the following command:
```shell
protoc --proto_path=input_dir --python_out=output_dir input_dir/*.proto
```
