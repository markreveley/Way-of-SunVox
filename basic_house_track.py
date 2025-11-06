#!/usr/bin/env python3
"""
Generate a complete basic house track in SunVox
- 125 BPM
- Four-on-the-floor kick
- Hi-hats and percussion
- Bassline
- Chord progression
- Simple lead melody
- Full arrangement structure
"""

from rv.api import Project, Pattern, m, NOTE, NOTECMD

print("Creating basic house track...")

# Create project
p = Project()
p.name = "Basic House Track"
p.initial_bpm = 125
p.initial_tpl = 6

# ============================================================================
# DRUMS
# ============================================================================

# Kick drum - four on the floor
kick = p.new_module(
    m.Kicker,
    name="Kick",
    vol=256,
    boost=200,
    release=100,
    x=256,
    y=128,
    color=(255, 80, 80)
)

# Hi-hat (using DrumSynth)
drums = p.new_module(
    m.DrumSynth,
    name="Drums",
    bass_volume=0,  # No bass drum
    hihat_volume=220,
    snare_volume=180,
    x=384,
    y=128,
    color=(255, 200, 80)
)

# Clap (using another DrumSynth)
clap = p.new_module(
    m.DrumSynth,
    name="Clap",
    bass_volume=0,
    hihat_volume=0,
    snare_volume=200,
    snare_panning=0,
    x=512,
    y=128,
    color=(200, 255, 80)
)

# ============================================================================
# BASS
# ============================================================================

# Sub bass
bass = p.new_module(
    m.AnalogGenerator,
    name="Sub Bass",
    waveform=m.AnalogGenerator.Waveform.sin,
    volume=220,
    attack=5,
    release=150,
    sustain=True,
    filter=m.AnalogGenerator.Filter.lp_12db,
    filter_cutoff=100,
    x=256,
    y=256,
    color=(80, 120, 255)
)

# Bass compression
bass_comp = p.new_module(
    m.Compressor,
    name="Bass Comp",
    volume=256,
    threshold=180,
    slope=0,
    attack=5,
    release=100,
    x=384,
    y=256,
    color=(100, 150, 255)
)

# ============================================================================
# CHORDS
# ============================================================================

# Chord synth (FM for that classic house sound)
chords = p.new_module(
    m.Fm,
    name="Chords",
    c_volume=180,
    m_volume=120,
    c_freq_ratio=1,  # 1:1 (0-16 range)
    m_freq_ratio=2,  # 2:1 (0-16 range)
    attack=150,
    release=200,
    sustain=True,
    x=256,
    y=384,
    color=(180, 120, 255)
)

# Chord filter for movement
chord_filter = p.new_module(
    m.Filter,
    name="Chord Filter",
    type=m.Filter.Type.lp,
    freq=180,
    resonance=100,
    x=384,
    y=384,
    color=(200, 140, 255)
)

# Chord reverb
chord_reverb = p.new_module(
    m.Reverb,
    name="Chord Reverb",
    volume=256,
    dryout=180,
    wetout=100,
    x=512,
    y=384,
    color=(220, 160, 255)
)

# ============================================================================
# LEAD
# ============================================================================

# Simple lead synth
lead = p.new_module(
    m.AnalogGenerator,
    name="Lead",
    waveform=m.AnalogGenerator.Waveform.saw,
    volume=160,
    attack=50,
    release=180,
    sustain=True,
    filter=m.AnalogGenerator.Filter.lp_12db,
    filter_cutoff=200,
    x=256,
    y=512,
    color=(255, 180, 100)
)

# Lead delay
lead_delay = p.new_module(
    m.Delay,
    name="Lead Delay",
    volume=256,
    delay_l=6,  # 1/8 note
    delay_r=6,
    channels=m.Delay.Channels.stereo,
    x=384,
    y=512,
    color=(255, 200, 120)
)

# ============================================================================
# MASTER EFFECTS
# ============================================================================

# Master compressor (glue)
master_comp = p.new_module(
    m.Compressor,
    name="Master Comp",
    volume=256,
    threshold=190,
    slope=0,
    attack=10,
    release=150,
    x=640,
    y=300,
    color=(255, 255, 100)
)

# ============================================================================
# CONNECTIONS
# ============================================================================

# Drums to output
kick >> master_comp
drums >> master_comp
clap >> master_comp

# Bass chain
bass >> bass_comp >> master_comp

# Chord chain
chords >> chord_filter >> chord_reverb >> master_comp

# Lead chain
lead >> lead_delay >> master_comp

# Master to output
master_comp >> p.output

# ============================================================================
# PATTERNS
# ============================================================================

print("Creating patterns...")

# Pattern 1: Kick (4 on the floor)
kick_pattern = Pattern(name="Kick", lines=32, tracks=1)
p.attach_pattern(kick_pattern)
for line in [0, 8, 16, 24]:
    kick_pattern.data[line][0].note = NOTE.C5
    kick_pattern.data[line][0].vel = 120
    kick_pattern.data[line][0].module = kick.index + 1

# Pattern 2: Hi-hats (8th notes closed, 16th notes open)
hihat_pattern = Pattern(name="Hihats", lines=32, tracks=1)
p.attach_pattern(hihat_pattern)
# Closed hats every 4 lines (8th notes)
for line in range(0, 32, 4):
    hihat_pattern.data[line][0].note = NOTE.C5
    hihat_pattern.data[line][0].vel = 90
    hihat_pattern.data[line][0].module = drums.index + 1
# Open hats on offbeats
for line in [6, 14, 22, 30]:
    hihat_pattern.data[line][0].note = NOTE.C5
    hihat_pattern.data[line][0].vel = 110
    hihat_pattern.data[line][0].module = drums.index + 1

# Pattern 3: Claps (beats 2 and 4)
clap_pattern = Pattern(name="Claps", lines=32, tracks=1)
p.attach_pattern(clap_pattern)
for line in [8, 24]:
    clap_pattern.data[line][0].note = NOTE.C5
    clap_pattern.data[line][0].vel = 100
    clap_pattern.data[line][0].module = clap.index + 1

# Pattern 4: Bassline (Am-F-C-G progression in bass)
bass_pattern = Pattern(name="Bassline", lines=128, tracks=1)
p.attach_pattern(bass_pattern)
# Am (A)
bass_pattern.data[0][0].note = NOTE.A2
bass_pattern.data[0][0].vel = 100
bass_pattern.data[0][0].module = bass.index + 1
bass_pattern.data[14][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[14][0].module = bass.index + 1

bass_pattern.data[16][0].note = NOTE.A2
bass_pattern.data[16][0].vel = 100
bass_pattern.data[16][0].module = bass.index + 1
bass_pattern.data[30][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[30][0].module = bass.index + 1

# F (F)
bass_pattern.data[32][0].note = NOTE.F2
bass_pattern.data[32][0].vel = 100
bass_pattern.data[32][0].module = bass.index + 1
bass_pattern.data[46][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[46][0].module = bass.index + 1

bass_pattern.data[48][0].note = NOTE.F2
bass_pattern.data[48][0].vel = 100
bass_pattern.data[48][0].module = bass.index + 1
bass_pattern.data[62][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[62][0].module = bass.index + 1

# C (C)
bass_pattern.data[64][0].note = NOTE.C3
bass_pattern.data[64][0].vel = 100
bass_pattern.data[64][0].module = bass.index + 1
bass_pattern.data[78][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[78][0].module = bass.index + 1

bass_pattern.data[80][0].note = NOTE.C3
bass_pattern.data[80][0].vel = 100
bass_pattern.data[80][0].module = bass.index + 1
bass_pattern.data[94][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[94][0].module = bass.index + 1

# G (G)
bass_pattern.data[96][0].note = NOTE.G2
bass_pattern.data[96][0].vel = 100
bass_pattern.data[96][0].module = bass.index + 1
bass_pattern.data[110][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[110][0].module = bass.index + 1

bass_pattern.data[112][0].note = NOTE.G2
bass_pattern.data[112][0].vel = 100
bass_pattern.data[112][0].module = bass.index + 1
bass_pattern.data[126][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[126][0].module = bass.index + 1

# Pattern 5: Chord progression (Am-F-C-G)
chord_pattern = Pattern(name="Chords", lines=128, tracks=3)
p.attach_pattern(chord_pattern)

# Am chord (A-C-E) - 32 lines
chord_pattern.data[0][0].note = NOTE.A3
chord_pattern.data[0][0].vel = 80
chord_pattern.data[0][0].module = chords.index + 1
chord_pattern.data[0][1].note = NOTE.C4
chord_pattern.data[0][1].vel = 75
chord_pattern.data[0][1].module = chords.index + 1
chord_pattern.data[0][2].note = NOTE.E4
chord_pattern.data[0][2].vel = 75
chord_pattern.data[0][2].module = chords.index + 1

# F chord (F-A-C) - at line 32
chord_pattern.data[32][0].note = NOTE.F3
chord_pattern.data[32][0].vel = 80
chord_pattern.data[32][0].module = chords.index + 1
chord_pattern.data[32][1].note = NOTE.A3
chord_pattern.data[32][1].vel = 75
chord_pattern.data[32][1].module = chords.index + 1
chord_pattern.data[32][2].note = NOTE.C4
chord_pattern.data[32][2].vel = 75
chord_pattern.data[32][2].module = chords.index + 1

# C chord (C-E-G) - at line 64
chord_pattern.data[64][0].note = NOTE.C4
chord_pattern.data[64][0].vel = 80
chord_pattern.data[64][0].module = chords.index + 1
chord_pattern.data[64][1].note = NOTE.E4
chord_pattern.data[64][1].vel = 75
chord_pattern.data[64][1].module = chords.index + 1
chord_pattern.data[64][2].note = NOTE.G4
chord_pattern.data[64][2].vel = 75
chord_pattern.data[64][2].module = chords.index + 1

# G chord (G-B-D) - at line 96
chord_pattern.data[96][0].note = NOTE.G3
chord_pattern.data[96][0].vel = 80
chord_pattern.data[96][0].module = chords.index + 1
chord_pattern.data[96][1].note = NOTE.B3
chord_pattern.data[96][1].vel = 75
chord_pattern.data[96][1].module = chords.index + 1
chord_pattern.data[96][2].note = NOTE.D4
chord_pattern.data[96][2].vel = 75
chord_pattern.data[96][2].module = chords.index + 1

# Pattern 6: Simple lead melody
lead_pattern = Pattern(name="Lead Melody", lines=64, tracks=1)
p.attach_pattern(lead_pattern)

# Simple melody over Am-F
melody_notes = [
    (0, NOTE.E5, 90),
    (8, NOTE.C5, 85),
    (16, NOTE.A4, 90),
    (24, NOTE.C5, 85),
    (32, NOTE.F5, 90),
    (40, NOTE.E5, 85),
    (48, NOTE.C5, 90),
    (56, NOTE.A4, 85),
]

for line, note, vel in melody_notes:
    lead_pattern.data[line][0].note = note
    lead_pattern.data[line][0].vel = vel
    lead_pattern.data[line][0].module = lead.index + 1
    # Note off after 6 lines
    if line + 6 < 64:
        lead_pattern.data[line + 6][0].note = NOTECMD.NOTE_OFF
        lead_pattern.data[line + 6][0].module = lead.index + 1

# Pattern 7: Intro kick only (for build-up)
intro_kick = Pattern(name="Intro Kick", lines=32, tracks=1)
p.attach_pattern(intro_kick)
for line in [0, 8, 16, 24]:
    intro_kick.data[line][0].note = NOTE.C5
    intro_kick.data[line][0].vel = 100  # Softer
    intro_kick.data[line][0].module = kick.index + 1

print(f"✓ Created {len(p.patterns)} patterns")

# ============================================================================
# SAVE
# ============================================================================

output_path = "/home/user/Way-of-SunVox/basic_house_track.sunvox"
with open(output_path, 'wb') as f:
    p.write_to(f)

print(f"\n{'='*60}")
print(f"✓ Basic house track created successfully!")
print(f"{'='*60}")
print(f"File: {output_path}")
print(f"BPM: {p.initial_bpm}")
print(f"Modules: {len([m for m in p.modules if m is not None])}")
print(f"Patterns: {len(p.patterns)}")
print(f"\nArrangement Guide:")
print(f"  Patterns 0-6 contain:")
print(f"    0: Kick (four-on-the-floor)")
print(f"    1: Hi-hats (8th notes)")
print(f"    2: Claps (2 & 4)")
print(f"    3: Bassline (Am-F-C-G)")
print(f"    4: Chords (Am-F-C-G)")
print(f"    5: Lead melody")
print(f"    6: Intro kick (softer)")
print(f"\nSuggested Arrangement:")
print(f"  - Start with pattern 6 (intro kick) for 4 bars")
print(f"  - Add patterns 0,1 for 4 bars")
print(f"  - Add pattern 3 (bass) for build")
print(f"  - Drop: All patterns 0-5 together")
print(f"  - Breakdown: Just patterns 4,5 (chords + lead)")
print(f"  - Final drop: All patterns again")
print(f"{'='*60}")
