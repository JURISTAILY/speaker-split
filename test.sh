source venv/bin/activate

python yandex/asrclient-cli.py \
    --key="d0f636aa-b10a-495d-ae5a-c56459497c1c" \
    --server="asr.yandex.net"  \
    --port="80" \
    --format="audio/x-pcm;bit=16;rate=16000" \
    --model="freeform" \
    --lang="ru-RU" \
    --inter-utt-silence="1.2" \
    --silent \
    --capitalize \
    audio_samples/sound9.wav

deactivate
