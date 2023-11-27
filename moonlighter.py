# moonlighter, the miniature beep-boop midi player for python
# flyingfathead (& chaoswhisperer) // nov 26 2023
# https://github.com/FlyingFathead/moonlighter

version_num = "1.16"

import os
import shutil
import sys
import subprocess
import argparse
import threading
import time

# Global flag to indicate skip
skip_flag = False

def listen_for_skip():
    global skip_flag
    input("Press <CTRL-C> to skip the current movement...")
    skip_flag = True

def lazy_imports():
    global np, sd, sf, mido, AudioSegment
    import numpy as np
    import sounddevice as sd
    import soundfile as sf
    import mido
    import requests
    from pydub import AudioSegment

# print term width horizontal line
def h_line(character='-'):
    terminal_width = shutil.get_terminal_size().columns
    line = character * terminal_width
    print(line, flush=True)

def install_packages():
    packages = ["numpy", "sounddevice", "soundfile", "mido", "pydub", "requests"]
    for package in packages:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def download_midi(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

def midi_to_freq(note):
    return 438.0 * (2.0 ** ((note - 69) / 12.0))

def generate_sine_wave(freq, duration, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    return np.sin(freq * t * 2 * np.pi)

def ticks_to_seconds(ticks, ticks_per_beat, tempo):
    return ticks / ticks_per_beat * (tempo / 1000000.0)

def read_and_process_midi(file_path, sample_rate=44100, dump=False, dump_file=None, note_length=1.0):
    global skip_flag
    lazy_imports()  # Ensure all required modules are imported    
    try:
        midi = mido.MidiFile(file_path)
        ticks_per_beat = midi.ticks_per_beat
        tempo = 500000  # Default MIDI tempo (120 BPM)
        max_time = 0  # For calculating buffer length

        # First pass to calculate max_time
        for track in midi.tracks:
            current_time = 0
            for msg in track:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                current_time += ticks_to_seconds(msg.time, ticks_per_beat, tempo)
                max_time = max(max_time, current_time)

        audio_buffer = np.zeros(int(max_time * sample_rate))

        # Second pass to process notes
        for track in midi.tracks:
            current_time = 0
            for msg in track:
                if msg.type == 'set_tempo':
                    tempo = msg.tempo
                current_time += ticks_to_seconds(msg.time, ticks_per_beat, tempo)

                if not msg.is_meta and msg.type == 'note_on' and msg.velocity > 0:
                    freq = midi_to_freq(msg.note)
                    # Use the provided note_length for the duration of each note
                    sine_wave = generate_sine_wave(freq, note_length, sample_rate)
                    start_index = int(current_time * sample_rate)
                    end_index = min(start_index + len(sine_wave), len(audio_buffer))
                    audio_buffer[start_index:end_index] += sine_wave[:end_index - start_index]

        audio_buffer = np.clip(audio_buffer, -1, 1)

        if dump:
            # Define output_file before using it in print statement
            output_file = dump_file if dump_file else file_path.rsplit('.', 1)[0] + '.mp3'
            h_line()
            print(f'Dumping audio to: {output_file} ...', flush=True)
            sf.write('temp.wav', audio_buffer, sample_rate)
            audio_segment = AudioSegment.from_wav('temp.wav')
            audio_segment.export(output_file, format='mp3')
            print(f'Audio dumped to: {output_file}', flush=True)
            h_line()
        else:
            sys.stdout.flush()  # Explicitly flush the output before playback            
            sd.play(audio_buffer, sample_rate)
            while sd.get_stream().active:  # Check if the stream is still playing
                if skip_flag:  # Check if the skip flag is set
                    sd.stop()  # Stop the playback
                    break
                time.sleep(0.1)  # Short sleep to prevent high CPU usage
    except KeyboardInterrupt:
        print("\nPlayback interrupted.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Moonlighter v{version_num} -- A Simple MIDI Sine Wave Player [2023 <> FlyingFathead (w/ ChaosWhisperer)]")
    parser.add_argument("midi_file", type=str, nargs='?', default=None, help="Path to the MIDI file. Required if not using --deploy.")
    parser.add_argument("--dump", nargs='?', const=True, default=False, help="Dump output to MP3. Optionally provide a filename for the MP3.")
    parser.add_argument("--deploy", action="store_true", help="Automatically deploy: Installs required packages, downloads 'Moonlight Sonata', and plays.")
    parser.add_argument("--notelength", type=float, default=1.0, help="Length of each note in seconds. Default is 1.0 seconds.")
    args = parser.parse_args()

    if args.deploy:
        h_line()
        print(f"::: Deploying Moonlighter v.{version_num}...")
        h_line()

        install_packages()

        h_line()
        print("""
            . - ^ ~ * ~ ^ - .
        , '                   ' ,
       :                        :
       :      .      .      .   :
       :    '   .  "   . '    ' :
       :   ~  MOONLIGHTER  ~    :
        : , '              ' , :
        ' .                 . '
            ' - . _ _ _ . - '

        Enjoy the Moonlight ...
        """, flush=True)
        h_line()
        print("[INFO] Press <CTRL-C> to skip a movement...", flush=True)
        h_line()

        # URLs for all three movements
        midi_urls = ["http://www.piano-midi.de/midis/beethoven/mond_1.mid",
                    "http://www.piano-midi.de/midis/beethoven/mond_2.mid",
                    "http://www.piano-midi.de/midis/beethoven/mond_3.mid"]
        midi_filenames = ["mond_1.mid", "mond_2.mid", "mond_3.mid"]

        # Download and play each movement
        for i, (url, filename) in enumerate(zip(midi_urls, midi_filenames), start=1):
            print(f"::: Downloading Moonlight Sonata, movement {i}...")
            download_midi(url, filename)
            print(f"::: Movement {i} downloaded: {filename}")

            # Adjust note length for the third movement
            notelength = 0.1 if i == 3 else args.notelength
            print(f"::: Playing Moonlight Sonata, movement {i}...")
            read_and_process_midi(filename, sample_rate=44100, dump=bool(args.dump), 
                                dump_file=args.dump if args.dump not in [True, False] else None, 
                                note_length=notelength)

        h_line()
    
    elif args.midi_file:
        lazy_imports()  # Import packages after installation
        # read_and_process_midi(args.midi_file, dump=bool(args.dump), dump_file=args.dump if args.dump not in [True, False] else None)
        read_and_process_midi(args.midi_file, sample_rate=44100, dump=bool(args.dump), 
                          dump_file=args.dump if args.dump not in [True, False] else None, 
                          note_length=args.notelength)
    else:
        parser.print_help()
