# Using Whiser as an interpret thansk to `whisper_mic`

[whisper_mic](https://github.com/mallorbc/whisper_mic) allows you to feed the microphone's input to Whisper locally in (almost) real time and transcribe it.

IMPORTANT: we are using my fork [ThibTrip/whisper_mic](https://github.com/mallorbc/whisper_mic) because the original repository does not support different tasks than transcription, while OpenAI Whisper's model can actually also translate (to English only). I added the possibility to change the task in my fork.

# Demo

1. Open one terminal and run a transcription task. Unless you have a strong computer with a good GPU, you should stick to the tiny or small model (do not forget to pass in `--device=cuda` if you are using a CUDA based GPU):

```
poetry shell
whisper_mic --model=small --task=transcribe --faster --loop
```

2. Open a second terminal and put both terminals side by side

```
poetry shell
whisper_mic --model=small --task=translate --faster --loop
```

3. Watch the magic (although don't expect too much if you use small models 🙈)
