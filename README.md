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
pip install -U numpy sounddevice soundfile mido pydub requests
```
(`requests` is only used by `--deploy`, but it's a recommended module)

Play with your favorite midi file:
```bash
python moonlighter.py /path/to/your/midi/file.mid
```

## Other features
Dump the midi to mp3:
```bash
python moonlighter.py /path/to/your/midi/file.mid --dump output.mp3
```
Adjust the beeps and boops, a.k.a. note length (in seconds):
```bash
python moonlighter.py /path/to/your/midi/file.mid --notelength 0.1
```
_(adjusts the note length to 0.1 sec)_

# Changelog
- `v1.16` - bug fixes, all three movements
- `v1.08` - small bug fixes (mp3 export bug)
- `v1.07` - Note length adjustment with `--notelength` added

# Info
- by FlyingFathead (w/ ghostcode by ChaosWhisperer)
- https://github.com/FlyingFathead/moonlighter/
