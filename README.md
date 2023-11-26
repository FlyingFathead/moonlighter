# moonlighter
Miniature beep-boop MIDI player for Python. Good for audio alerts, debugging and such!

# Usage
First, clone the repo with:
```bash
git clone https://github.com/FlyingFathead/moonlighter
```
then:
```bash
cd moonlighter
```

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
- by FlyingFathead (w/ ghostcode by ChaosWhisperer)
- https://github.com/FlyingFathead/moonlighter/
