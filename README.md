# moonlighter
Miniature beep-boop MIDI player for Python

# Usage
## Quick deployment 
(installs all required Python packages, downloads 'Moonlight Sonata' and plays it):
```bash
python moonlighter.py --deploy
```
## Slow deployment:
```bash
pip install -U numpy sounddevice soundfile mido pydub
```
Play with your favorite midi file:
```bash
python moonlighter.py /path/to/your/midi/file.mid
```
Dump the midi to mp3:
```bash
python moonlighter.py /path/to/your/midi/file.mid --dump output.mp3
```

# Info
