from mido import MidiFile

# -------- SETTINGS --------
MIDI_FILE = "Super Mario Bros. 1 -  Overworld Theme.mid"
DEFAULT_TEMPO = 500000  # default 120 BPM in microseconds
NOTE_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

# -------- HELPER FUNCTIONS --------
def note_number_to_name(note):
    octave = (note // 12) - 1
    name = NOTE_NAMES[note % 12]
    return f"{name}{octave}"

def ticks_to_beats(ticks, ticks_per_beat):
    return ticks / ticks_per_beat

# -------- MAIN PARSING --------
mid = MidiFile(MIDI_FILE)
ticks_per_beat = mid.ticks_per_beat

melody = []
tempo = DEFAULT_TEMPO
found = False

for i, track in enumerate(mid.tracks):
    time_acc = 0
    this_melody = []

    for msg in track:
        if msg.type == 'set_tempo':
            tempo = msg.tempo
        if msg.time > 0:
            time_acc += msg.time
        if msg.type == 'note_on' and msg.velocity > 0:
            note = note_number_to_name(msg.note)
            beats = ticks_to_beats(time_acc, ticks_per_beat)
            duration = max(1, round(beats * 4))  # convert to quarter-note units
            this_melody.append(f"{note}:{duration}")
            time_acc = 0

    if len(this_melody) > 10:
        melody = this_melody
        print(f"✅ Using Track {i}: {track.name} — {len(melody)} notes found")
        found = True
        break

if not found:
    print("❌ No usable melody found in MIDI.")
    exit()

# -------- EXPORT FINAL CODE --------
with open("microbit_final_code.py", "w") as f:
    f.write("from microbit import *\nimport music\n\n")
    f.write("melody = [\n")
    for note in melody:
        f.write(f"    '{note}',\n")
    f.write("]\n\n")
    f.write("music.set_tempo(bpm=140)\n")
    f.write("music.play(melody)\n")
print("🎉 microbit_final_code.py has been generated.")
