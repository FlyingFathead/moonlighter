# moonlighter
Miniature beep-boop MIDI player for Python. Good for audio alerts, debugging and such!

## Usage
Single-line install for *nix + Git Bash (installs all required Python packages, downloads 'Moonlight Sonata' and plays it):
```bash
git clone https://github.com/FlyingFathead/moonlighter/ && cd moonlighter && python moonlighter.py --deploy
```

## Slow deployment:
First, clone the repo with:
```bash
git clone https://github.com/FlyingFathead/moonlighter
```
then:
```bash
cd moonlighter
```
install the prerequisite `pip` packages:
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
