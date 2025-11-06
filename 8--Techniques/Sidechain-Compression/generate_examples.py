#!/usr/bin/env python3
"""
Generate SunVox example files for Sidechain Compression tutorial
"""

from rv.api import Project, Pattern, m, NOTE, NOTECMD
import os

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

print("Generating SunVox sidechain compression examples...")

# ==============================================================================
# Example 1: Basic EDM Kick-to-Bass Sidechain
# ==============================================================================
print("\n1. Creating sidechain_basic_edm.sunvox...")

p1 = Project()
p1.sunvox_version = (1, 9, 3, 1)  # Compatible with SunVox 1.9.3
p1.based_on_version = (1, 9, 3, 1)
p1.name = "Sidechain - Basic EDM"
p1.initial_bpm = 128
p1.initial_tpl = 6

# Create kick drum (Kicker module)
kick = p1.new_module(
    m.Kicker,
    name="Kick",
    vol=256,  # Full volume
    boost=256,
    x=256,
    y=256,
    color=(255, 80, 80)  # Red
)

# Create bass synth (Analog Generator with saw wave)
bass = p1.new_module(
    m.AnalogGenerator,
    name="Bass",
    waveform=m.AnalogGenerator.Waveform.saw,
    volume=192,
    attack=0,
    release=200,
    sustain=True,
    x=512,
    y=128,
    color=(80, 180, 255)  # Blue
)

# Create compressor for sidechain effect
comp = p1.new_module(
    m.Compressor,
    name="Sidechain Comp",
    volume=256,
    threshold=154,  # ~-20dB (256 = 0dB, lower = more negative)
    slope=0,  # Fast
    attack=1,
    release=100,
    mode=m.Compressor.Mode.peak,
    x=640,
    y=128,
    color=(80, 255, 180)  # Green
)

# Create Sound2Ctl to convert kick audio to control signal
s2c = p1.new_module(
    m.Sound2Ctl,
    name="SC Trigger",
    absolute=True,
    gain=200,
    smooth=10,
    sample_rate_hz=100,
    channels=m.Sound2Ctl.Channels.stereo,
    x=384,
    y=256,
    color=(255, 200, 80)  # Orange
)

# Connect modules
# Bass -> Compressor -> Output
bass >> comp >> p1.output

# Kick -> Output (for audio)
kick >> p1.output

# Kick -> Sound2Ctl (for sidechain trigger, no audio)
kick >> s2c

# Create a simple kick pattern (pattern 0)
kick_pattern = Pattern(name="Kick", tracks=1, lines=32)
p1.attach_pattern(kick_pattern)
# Four-on-the-floor kick pattern
for line in [0, 8, 16, 24]:
    kick_pattern.data[line][0].note = NOTE.C5
    kick_pattern.data[line][0].vel = 128
    kick_pattern.data[line][0].module = kick.index + 1

# Create a bass pattern (pattern 1)
bass_pattern = Pattern(name="Bass", tracks=1, lines=32)
p1.attach_pattern(bass_pattern)
# Simple bass note
bass_pattern.data[0][0].note = NOTE.C3
bass_pattern.data[0][0].vel = 100
bass_pattern.data[0][0].module = bass.index + 1
bass_pattern.data[30][0].note = NOTECMD.NOTE_OFF
bass_pattern.data[30][0].module = bass.index + 1

# Save the project
output_path = os.path.join(script_dir, "sidechain_basic_edm.sunvox")
with open(output_path, 'wb') as f:
    p1.write_to(f)
print(f"   ✓ Created: {output_path}")


# ==============================================================================
# Example 2: Vocal Clarity (Subtle Sidechain)
# ==============================================================================
print("\n2. Creating sidechain_vocal_clarity.sunvox...")

p2 = Project()
p2.sunvox_version = (1, 9, 3, 1)  # Compatible with SunVox 1.9.3
p2.based_on_version = (1, 9, 3, 1)
p2.name = "Sidechain - Vocal Clarity"
p2.initial_bpm = 90
p2.initial_tpl = 6

# Create a simple trigger (simulating vocal timing)
vocal_trigger = p2.new_module(
    m.Kicker,
    name="Vocal Trigger",
    vol=0,  # Silent - just for trigger
    x=256,
    y=256,
    color=(255, 180, 255)  # Pink
)

# Create pad synth (representing music bed)
pad = p2.new_module(
    m.AnalogGenerator,
    name="Music Pad",
    waveform=m.AnalogGenerator.Waveform.saw,
    volume=180,
    attack=200,
    release=256,
    sustain=True,
    filter=m.AnalogGenerator.Filter.lp_12db,
    filter_cutoff=180,
    x=512,
    y=128,
    color=(150, 120, 255)  # Purple
)

# Create subtle compressor
subtle_comp = p2.new_module(
    m.Compressor,
    name="Gentle Duck",
    volume=256,
    threshold=180,  # Higher threshold for subtlety
    slope=0,
    attack=8,  # Slower attack
    release=200,  # Longer release
    mode=m.Compressor.Mode.peak,
    x=640,
    y=128,
    color=(80, 255, 180)  # Green
)

# Create Sound2Ctl for trigger
s2c_vocal = p2.new_module(
    m.Sound2Ctl,
    name="Vocal SC",
    absolute=True,
    gain=120,  # Lower gain for subtle effect
    smooth=30,
    x=384,
    y=256,
    color=(255, 200, 80)
)

# Connect: Pad -> Compressor -> Output
pad >> subtle_comp >> p2.output

# Vocal trigger -> Sound2Ctl
vocal_trigger >> s2c_vocal

# Create patterns
trigger_pattern = Pattern(name="Vocal Timing", tracks=1, lines=64)
p2.attach_pattern(trigger_pattern)
# Simulate vocal phrases
for line in [0, 16, 32, 48]:
    trigger_pattern.data[line][0].note = NOTE.C5
    trigger_pattern.data[line][0].vel = 80
    trigger_pattern.data[line][0].module = vocal_trigger.index + 1

pad_pattern = Pattern(name="Pad", tracks=1, lines=64)
p2.attach_pattern(pad_pattern)
# Sustained chord
pad_pattern.data[0][0].note = NOTE.C4
pad_pattern.data[0][0].vel = 80
pad_pattern.data[0][0].module = pad.index + 1

output_path = os.path.join(script_dir, "sidechain_vocal_clarity.sunvox")
with open(output_path, 'wb') as f:
    p2.write_to(f)
print(f"   ✓ Created: {output_path}")


# ==============================================================================
# Example 3: Rhythmic Gating (Extreme Sidechain)
# ==============================================================================
print("\n3. Creating sidechain_rhythmic_gate.sunvox...")

p3 = Project()
p3.name = "Sidechain - Rhythmic Gate"
p3.initial_bpm = 140
p3.initial_tpl = 6

# Hi-hat trigger for rhythmic pattern
hihat = p3.new_module(
    m.DrumSynth,
    name="HiHat Trigger",
    vol=128,
    bass_panning=-128,
    hihat_volume=256,
    x=256,
    y=256,
    color=(255, 255, 80)  # Yellow
)

# Pad to be gated
gate_pad = p3.new_module(
    m.AnalogGenerator,
    name="Gated Pad",
    waveform=m.AnalogGenerator.Waveform.triangle,
    volume=200,
    attack=0,
    release=256,
    sustain=True,
    x=512,
    y=128,
    color=(255, 120, 200)  # Pink
)

# Extreme compressor for gating
gate_comp = p3.new_module(
    m.Compressor,
    name="Gate Comp",
    volume=256,
    threshold=100,  # Very low threshold
    slope=0,  # Fast
    attack=0,  # Instant
    release=20,  # Very fast release
    mode=m.Compressor.Mode.peak,
    x=640,
    y=128,
    color=(255, 80, 80)  # Red
)

# Sound2Ctl for extreme effect
s2c_gate = p3.new_module(
    m.Sound2Ctl,
    name="Gate Trigger",
    absolute=True,
    gain=255,  # Maximum gain
    smooth=0,  # No smoothing for sharp gates
    x=384,
    y=256,
    color=(255, 200, 80)
)

# Connections
gate_pad >> gate_comp >> p3.output
hihat >> p3.output
hihat >> s2c_gate

# Create rhythmic hi-hat pattern
hihat_pattern = Pattern(name="HiHat", tracks=1, lines=16)
p3.attach_pattern(hihat_pattern)
# 16th note hi-hats
for line in range(0, 16, 2):
    hihat_pattern.data[line][0].note = NOTE.C5
    hihat_pattern.data[line][0].vel = 100
    hihat_pattern.data[line][0].module = hihat.index + 1

# Sustained pad
gatepad_pattern = Pattern(name="Pad", tracks=1, lines=16)
p3.attach_pattern(gatepad_pattern)
gatepad_pattern.data[0][0].note = NOTE.E3
gatepad_pattern.data[0][0].vel = 100
gatepad_pattern.data[0][0].module = gate_pad.index + 1

output_path = os.path.join(script_dir, "sidechain_rhythmic_gate.sunvox")
with open(output_path, 'wb') as f:
    p3.write_to(f)
print(f"   ✓ Created: {output_path}")


# ==============================================================================
# Example 4: Multi-Band Sidechain
# ==============================================================================
print("\n4. Creating sidechain_multiband.sunvox...")

p4 = Project()
p4.name = "Sidechain - Multi-Band"
p4.initial_bpm = 120
p4.initial_tpl = 6

# Kick for trigger
mb_kick = p4.new_module(
    m.Kicker,
    name="Kick",
    vol=256,
    x=256,
    y=384,
    color=(255, 80, 80)
)

# Rich pad with multiple frequencies
rich_pad = p4.new_module(
    m.AnalogGenerator,
    name="Rich Pad",
    waveform=m.AnalogGenerator.Waveform.saw,
    volume=180,
    attack=150,
    release=250,
    sustain=True,
    x=256,
    y=128,
    color=(180, 140, 255)
)

# Low-pass filter for low band
lowband_filter = p4.new_module(
    m.Filter,
    name="Low Band",
    type=m.Filter.Type.lp,
    freq=300,
    resonance=0,
    x=384,
    y=64,
    color=(255, 100, 100)
)

# High-pass filter for high band (unchanged)
highband_filter = p4.new_module(
    m.Filter,
    name="High Band",
    type=m.Filter.Type.hp,
    freq=300,
    resonance=0,
    x=384,
    y=192,
    color=(100, 200, 255)
)

# Compressor only on low band
lowband_comp = p4.new_module(
    m.Compressor,
    name="Low Band Comp",
    volume=256,
    threshold=160,
    slope=0,
    attack=1,
    release=120,
    x=512,
    y=64,
    color=(80, 255, 180)
)

# Sound2Ctl
s2c_mb = p4.new_module(
    m.Sound2Ctl,
    name="SC Trigger",
    absolute=True,
    gain=180,
    x=384,
    y=384,
    color=(255, 200, 80)
)

# Connections
# Pad splits into two bands
rich_pad >> lowband_filter >> lowband_comp >> p4.output
rich_pad >> highband_filter >> p4.output

# Kick audio and trigger
mb_kick >> p4.output
mb_kick >> s2c_mb

# Patterns
mb_kick_pattern = Pattern(name="Kick", tracks=1, lines=32)
p4.attach_pattern(mb_kick_pattern)
for line in [0, 8, 16, 24]:
    mb_kick_pattern.data[line][0].note = NOTE.C5
    mb_kick_pattern.data[line][0].vel = 120
    mb_kick_pattern.data[line][0].module = mb_kick.index + 1

mb_pad_pattern = Pattern(name="Pad", tracks=1, lines=32)
p4.attach_pattern(mb_pad_pattern)
mb_pad_pattern.data[0][0].note = NOTE.A3
mb_pad_pattern.data[0][0].vel = 90
mb_pad_pattern.data[0][0].module = rich_pad.index + 1

output_path = os.path.join(script_dir, "sidechain_multiband.sunvox")
with open(output_path, 'wb') as f:
    p4.write_to(f)
print(f"   ✓ Created: {output_path}")


# ==============================================================================
# Example 5: Inverse Sidechain (Swelling)
# ==============================================================================
print("\n5. Creating sidechain_inverse.sunvox...")

p5 = Project()
p5.name = "Sidechain - Inverse Swell"
p5.initial_bpm = 128
p5.initial_tpl = 6

# Kick trigger
inv_kick = p5.new_module(
    m.Kicker,
    name="Kick",
    vol=256,
    x=256,
    y=256,
    color=(255, 80, 80)
)

# White noise for swelling effect
noise = p5.new_module(
    m.Generator,
    name="Noise",
    volume=160,
    waveform=m.Generator.Waveform.noise,
    x=512,
    y=128,
    color=(200, 200, 200)
)

# Amplifier to control swell (instead of ducking)
amp = p5.new_module(
    m.Amplifier,
    name="Swell Amp",
    volume=80,  # Start low
    inverse=False,
    x=640,
    y=128,
    color=(255, 180, 80)
)

# Sound2Ctl for inverse trigger
s2c_inv = p5.new_module(
    m.Sound2Ctl,
    name="Swell Trigger",
    absolute=True,
    gain=200,
    smooth=50,  # Smooth swelling
    x=384,
    y=256,
    color=(255, 200, 80)
)

# Connections
noise >> amp >> p5.output
inv_kick >> p5.output
inv_kick >> s2c_inv

# Patterns
inv_kick_pattern = Pattern(name="Kick", tracks=1, lines=32)
p5.attach_pattern(inv_kick_pattern)
for line in [0, 8, 16, 24]:
    inv_kick_pattern.data[line][0].note = NOTE.C5
    inv_kick_pattern.data[line][0].vel = 128
    inv_kick_pattern.data[line][0].module = inv_kick.index + 1

output_path = os.path.join(script_dir, "sidechain_inverse.sunvox")
with open(output_path, 'wb') as f:
    p5.write_to(f)
print(f"   ✓ Created: {output_path}")


# ==============================================================================
# Example 6: LFO Fake Sidechain
# ==============================================================================
print("\n6. Creating sidechain_lfo_fake.sunvox...")

p6 = Project()
p6.name = "Sidechain - LFO Fake"
p6.initial_bpm = 128
p6.initial_tpl = 6

# Bass synth
lfo_bass = p6.new_module(
    m.AnalogGenerator,
    name="Bass",
    waveform=m.AnalogGenerator.Waveform.saw,
    volume=200,
    attack=0,
    release=256,
    sustain=True,
    x=384,
    y=128,
    color=(80, 180, 255)
)

# LFO to create pumping effect
lfo = p6.new_module(
    m.Lfo,
    name="Pump LFO",
    volume=256,
    waveform=m.Lfo.Waveform.saw,
    freq=128,  # Synced to tempo
    duty_cycle=64,  # Sharp downward saw for pump
    generator=False,
    x=256,
    y=128,
    color=(255, 220, 80)
)

# Amplifier controlled by LFO
lfo_amp = p6.new_module(
    m.Amplifier,
    name="LFO Pump",
    volume=256,
    x=512,
    y=128,
    color=(180, 255, 180)
)

# Connections
lfo >> lfo_bass  # LFO modulates bass
lfo_bass >> lfo_amp >> p6.output

# Pattern
lfo_bass_pattern = Pattern(name="Bass", tracks=1, lines=32)
p6.attach_pattern(lfo_bass_pattern)
lfo_bass_pattern.data[0][0].note = NOTE.C3
lfo_bass_pattern.data[0][0].vel = 100
lfo_bass_pattern.data[0][0].module = lfo_bass.index + 1

output_path = os.path.join(script_dir, "sidechain_lfo_fake.sunvox")
with open(output_path, 'wb') as f:
    p6.write_to(f)
print(f"   ✓ Created: {output_path}")

print("\n" + "="*60)
print("✓ All 6 sidechain example files generated successfully!")
print("="*60)
