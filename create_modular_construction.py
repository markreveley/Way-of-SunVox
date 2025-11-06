#!/usr/bin/env python3
"""
Modular SunVox Construction - Layer by Layer

This demonstrates hierarchical composition using MetaModules:
- Layer 1: Simple building blocks (individual instruments as .sunvox files)
- Layer 2: Combined sections (drum kit, bass section as .sunvox files)
- Layer 3: Final track that loads Layer 2 modules

Each .sunvox file is self-contained and reusable!
"""

from rv.api import Project, Pattern, m, NOTE, NOTECMD
import os

output_dir = "/home/user/Way-of-SunVox/modular_construction"
os.makedirs(output_dir, exist_ok=True)

print("="*60)
print("MODULAR SUNVOX CONSTRUCTION")
print("Building complexity layer by layer...")
print("="*60)

# ============================================================================
# LAYER 1: SIMPLE BUILDING BLOCKS
# ============================================================================
print("\n[LAYER 1] Creating simple building blocks...")

# --- Building Block 1: Kick Drum ---
print("  1a. Kick drum module...")
kick_module = Project()
kick_module.name = "Kick Module"

kick = kick_module.new_module(
    m.Kicker,
    name="Kick",
    vol=256,
    boost=220,
    release=100,
    x=256,
    y=256,
    color=(255, 80, 80)
)

# Add compression for punch
kick_comp = kick_module.new_module(
    m.Compressor,
    name="Kick Comp",
    volume=256,
    threshold=170,
    slope=0,
    attack=1,
    release=80,
    x=384,
    y=256,
    color=(255, 120, 120)
)

kick >> kick_comp >> kick_module.output

# Simple pattern
kick_pattern = Pattern(name="Four on Floor", lines=32, tracks=1)
kick_module.attach_pattern(kick_pattern)
for line in [0, 8, 16, 24]:
    kick_pattern.data[line][0].note = NOTE.C5
    kick_pattern.data[line][0].vel = 120
    kick_pattern.data[line][0].module = kick.index + 1

with open(f"{output_dir}/layer1_kick.sunvox", 'wb') as f:
    kick_module.write_to(f)
print(f"    ✓ layer1_kick.sunvox")

# --- Building Block 2: Bass Synth ---
print("  1b. Bass synth module...")
bass_module = Project()
bass_module.name = "Bass Module"

bass = bass_module.new_module(
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

bass_filter = bass_module.new_module(
    m.Filter,
    name="Bass Filter",
    type=m.Filter.Type.lp,
    freq=120,
    resonance=80,
    x=384,
    y=256,
    color=(120, 160, 255)
)

bass >> bass_filter >> bass_module.output

# Bass pattern (A note)
bass_pattern = Pattern(name="Bass A", lines=32, tracks=1)
bass_module.attach_pattern(bass_pattern)
bass_pattern.data[0][0].note = NOTE.A2
bass_pattern.data[0][0].vel = 100
bass_pattern.data[0][0].module = bass.index + 1
bass_pattern.data[30][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[30][0].module = bass.index + 1

with open(f"{output_dir}/layer1_bass.sunvox", 'wb') as f:
    bass_module.write_to(f)
print(f"    ✓ layer1_bass.sunvox")

# --- Building Block 3: Chord Synth ---
print("  1c. Chord synth module...")
chord_module = Project()
chord_module.name = "Chord Module"

chord_synth = chord_module.new_module(
    m.Fm,
    name="FM Chords",
    c_volume=180,
    m_volume=100,
    c_freq_ratio=1,
    m_freq_ratio=2,
    attack=120,
    release=180,
    sustain=True,
    x=256,
    y=256,
    color=(180, 120, 255)
)

chord_reverb = chord_module.new_module(
    m.Reverb,
    name="Reverb",
    volume=256,
    dryout=200,
    wetout=80,
    x=384,
    y=256,
    color=(200, 140, 255)
)

chord_synth >> chord_reverb >> chord_module.output

# Chord pattern (Am triad)
chord_pattern = Pattern(name="Am Chord", lines=32, tracks=3)
chord_module.attach_pattern(chord_pattern)
chord_pattern.data[0][0].note = NOTE.A3
chord_pattern.data[0][0].vel = 80
chord_pattern.data[0][0].module = chord_synth.index + 1
chord_pattern.data[0][1].note = NOTE.C4
chord_pattern.data[0][1].vel = 75
chord_pattern.data[0][1].module = chord_synth.index + 1
chord_pattern.data[0][2].note = NOTE.E4
chord_pattern.data[0][2].vel = 75
chord_pattern.data[0][2].module = chord_synth.index + 1

with open(f"{output_dir}/layer1_chords.sunvox", 'wb') as f:
    chord_module.write_to(f)
print(f"    ✓ layer1_chords.sunvox")

# --- Building Block 4: Hi-Hat ---
print("  1d. Hi-hat module...")
hihat_module = Project()
hihat_module.name = "HiHat Module"

hihat = hihat_module.new_module(
    m.DrumSynth,
    name="HiHats",
    bass_volume=0,
    hihat_volume=220,
    snare_volume=0,
    x=256,
    y=256,
    color=(255, 220, 100)
)

hihat >> hihat_module.output

# Hi-hat pattern (8th notes)
hihat_pattern = Pattern(name="Hats 8th", lines=32, tracks=1)
hihat_module.attach_pattern(hihat_pattern)
for line in range(0, 32, 4):
    hihat_pattern.data[line][0].note = NOTE.C5
    hihat_pattern.data[line][0].vel = 85
    hihat_pattern.data[line][0].module = hihat.index + 1

with open(f"{output_dir}/layer1_hihat.sunvox", 'wb') as f:
    hihat_module.write_to(f)
print(f"    ✓ layer1_hihat.sunvox")

print(f"\n  → Created 4 Layer 1 building blocks")

# ============================================================================
# LAYER 2: COMBINED SECTIONS (using MetaModules)
# ============================================================================
print("\n[LAYER 2] Combining building blocks into sections...")

# NOTE: In Radiant Voices, we can't directly load .sunvox files as MetaModules
# programmatically (that's a SunVox GUI operation). Instead, we'll create
# Layer 2 files that you can manually enhance by loading Layer 1 files.
# However, we CAN create the structure that demonstrates the concept.

# --- Section 1: Rhythm Section ---
print("  2a. Rhythm section (kick + hihat)...")
rhythm_section = Project()
rhythm_section.name = "Rhythm Section"
rhythm_section.initial_bpm = 125

# Create placeholders that represent where you'd load the Layer 1 modules
kick_meta = rhythm_section.new_module(
    m.Kicker,
    name="KICK (Load layer1_kick.sunvox here)",
    vol=256,
    boost=220,
    x=256,
    y=200,
    color=(255, 100, 100)
)

hihat_meta = rhythm_section.new_module(
    m.DrumSynth,
    name="HIHAT (Load layer1_hihat.sunvox here)",
    bass_volume=0,
    hihat_volume=220,
    snare_volume=0,
    x=256,
    y=320,
    color=(255, 220, 100)
)

# Mixer for rhythm section
rhythm_mix = rhythm_section.new_module(
    m.Amplifier,
    name="Rhythm Mix",
    volume=256,
    x=450,
    y=260,
    color=(200, 200, 200)
)

kick_meta >> rhythm_mix >> rhythm_section.output
hihat_meta >> rhythm_mix >> rhythm_section.output

# Patterns
kick_pat = Pattern(name="Kick Pattern", lines=32, tracks=1)
rhythm_section.attach_pattern(kick_pat)
for line in [0, 8, 16, 24]:
    kick_pat.data[line][0].note = NOTE.C5
    kick_pat.data[line][0].vel = 120
    kick_pat.data[line][0].module = kick_meta.index + 1

hihat_pat = Pattern(name="HiHat Pattern", lines=32, tracks=1)
rhythm_section.attach_pattern(hihat_pat)
for line in range(0, 32, 4):
    hihat_pat.data[line][0].note = NOTE.C5
    hihat_pat.data[line][0].vel = 85
    hihat_pat.data[line][0].module = hihat_meta.index + 1

with open(f"{output_dir}/layer2_rhythm_section.sunvox", 'wb') as f:
    rhythm_section.write_to(f)
print(f"    ✓ layer2_rhythm_section.sunvox")

# --- Section 2: Harmonic Section ---
print("  2b. Harmonic section (bass + chords)...")
harmonic_section = Project()
harmonic_section.name = "Harmonic Section"
harmonic_section.initial_bpm = 125

bass_meta = harmonic_section.new_module(
    m.AnalogGenerator,
    name="BASS (Load layer1_bass.sunvox here)",
    waveform=m.AnalogGenerator.Waveform.sin,
    volume=220,
    x=256,
    y=200,
    color=(100, 150, 255)
)

chords_meta = harmonic_section.new_module(
    m.Fm,
    name="CHORDS (Load layer1_chords.sunvox here)",
    c_volume=180,
    m_volume=100,
    x=256,
    y=320,
    color=(180, 140, 255)
)

harmonic_mix = harmonic_section.new_module(
    m.Amplifier,
    name="Harmonic Mix",
    volume=256,
    x=450,
    y=260,
    color=(200, 200, 200)
)

bass_meta >> harmonic_mix >> harmonic_section.output
chords_meta >> harmonic_mix >> harmonic_section.output

# Patterns for Am chord
bass_pat = Pattern(name="Bass A", lines=32, tracks=1)
harmonic_section.attach_pattern(bass_pat)
bass_pat.data[0][0].note = NOTE.A2
bass_pat.data[0][0].vel = 100
bass_pat.data[0][0].module = bass_meta.index + 1

chord_pat = Pattern(name="Am Chord", lines=32, tracks=3)
harmonic_section.attach_pattern(chord_pat)
chord_pat.data[0][0].note = NOTE.A3
chord_pat.data[0][0].vel = 80
chord_pat.data[0][0].module = chords_meta.index + 1
chord_pat.data[0][1].note = NOTE.C4
chord_pat.data[0][1].vel = 75
chord_pat.data[0][1].module = chords_meta.index + 1
chord_pat.data[0][2].note = NOTE.E4
chord_pat.data[0][2].vel = 75
chord_pat.data[0][2].module = chords_meta.index + 1

with open(f"{output_dir}/layer2_harmonic_section.sunvox", 'wb') as f:
    harmonic_section.write_to(f)
print(f"    ✓ layer2_harmonic_section.sunvox")

print(f"\n  → Created 2 Layer 2 combined sections")

# ============================================================================
# LAYER 3: FINAL TRACK (using Layer 2 sections)
# ============================================================================
print("\n[LAYER 3] Creating final track from Layer 2 sections...")

final_track = Project()
final_track.name = "Modular House Track - Layer 3"
final_track.initial_bpm = 125

# Placeholder for rhythm section MetaModule
rhythm_meta = final_track.new_module(
    m.Amplifier,
    name="RHYTHM SECTION (Load layer2_rhythm_section.sunvox)",
    volume=256,
    x=200,
    y=200,
    color=(255, 150, 150)
)

# Placeholder for harmonic section MetaModule
harmonic_meta = final_track.new_module(
    m.Amplifier,
    name="HARMONIC SECTION (Load layer2_harmonic_section.sunvox)",
    volume=230,
    x=200,
    y=350,
    color=(150, 180, 255)
)

# Master processing
master_comp = final_track.new_module(
    m.Compressor,
    name="Master Glue",
    volume=256,
    threshold=200,
    slope=0,
    attack=10,
    release=150,
    x=450,
    y=275,
    color=(255, 255, 150)
)

# Connect
rhythm_meta >> master_comp >> final_track.output
harmonic_meta >> master_comp >> final_track.output

# Patterns that would trigger the MetaModules
track_pattern = Pattern(name="Full Track", lines=128, tracks=2)
final_track.attach_pattern(track_pattern)

# Pattern data to trigger both sections
track_pattern.data[0][0].note = NOTE.C5
track_pattern.data[0][0].vel = 100
track_pattern.data[0][0].module = rhythm_meta.index + 1

track_pattern.data[0][1].note = NOTE.C5
track_pattern.data[0][1].vel = 100
track_pattern.data[0][1].module = harmonic_meta.index + 1

with open(f"{output_dir}/layer3_final_track.sunvox", 'wb') as f:
    final_track.write_to(f)
print(f"    ✓ layer3_final_track.sunvox")

print(f"\n  → Created final Layer 3 composition")

# ============================================================================
# SUMMARY & INSTRUCTIONS
# ============================================================================
print("\n" + "="*60)
print("✓ MODULAR CONSTRUCTION COMPLETE!")
print("="*60)
print(f"\nCreated hierarchical structure in: {output_dir}/")
print("\n📁 LAYER 1 - Building Blocks (4 files):")
print("  • layer1_kick.sunvox      - Kick drum + compression")
print("  • layer1_bass.sunvox      - Sub bass + filter")
print("  • layer1_chords.sunvox    - FM chords + reverb")
print("  • layer1_hihat.sunvox     - Hi-hat generator")
print("\n📁 LAYER 2 - Combined Sections (2 files):")
print("  • layer2_rhythm_section.sunvox   - Kick + HiHat combo")
print("  • layer2_harmonic_section.sunvox - Bass + Chords combo")
print("\n📁 LAYER 3 - Final Track (1 file):")
print("  • layer3_final_track.sunvox - Complete composition")

print("\n" + "="*60)
print("HOW TO USE THE MODULAR HIERARCHY:")
print("="*60)
print("""
1. LAYER 1 files are self-contained instruments
   → Can be used directly or loaded as MetaModules

2. TO ENHANCE LAYER 2 (manual step in SunVox):
   a) Open layer2_rhythm_section.sunvox in SunVox
   b) Delete the placeholder Kicker module
   c) Add MetaModule (right-click → New → MetaModule)
   d) In MetaModule, click LOAD and select layer1_kick.sunvox
   e) Repeat for the DrumSynth → load layer1_hihat.sunvox
   f) Save the enhanced file

   (Do the same for layer2_harmonic_section.sunvox)

3. TO ENHANCE LAYER 3 (manual step in SunVox):
   a) Open layer3_final_track.sunvox
   b) Replace placeholders with MetaModules
   c) Load layer2_rhythm_section.sunvox and layer2_harmonic_section.sunvox
   d) Now you have a 3-layer modular composition!

4. BENEFITS:
   ✓ Reusable components across projects
   ✓ Easy to swap out parts (try different kicks, etc.)
   ✓ Better organization for complex tracks
   ✓ Can version control each layer independently
   ✓ Share building blocks with others

5. WORKFLOW:
   - Build simple Layer 1 modules first
   - Test each module independently
   - Combine into Layer 2 sections
   - Assemble Layer 3 final track
   - Can go even deeper (Layer 4, 5, etc.)!
""")

print("="*60)
print("This demonstrates OBJECT-ORIENTED music composition!")
print("="*60)
