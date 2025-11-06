# Generative SunVox: Programmatic File Generation

_The teacher is as a needle, the disciple is as thread._

_- Miyamoto Musashi_

## Overview

This document details the technical process of **programmatically generating SunVox files** using Python and the Radiant Voices library. All tutorial examples, demonstration tracks, and modular components in this repository were created through code, not manually in the SunVox GUI.

## Why Generate Files Programmatically?

### Advantages

✅ **Reproducibility**: Run script → get identical result
✅ **Version Control**: Track changes in code, not binary files
✅ **Parameterization**: Generate variations by changing values
✅ **Documentation**: Code explains what's being created
✅ **Batch Creation**: Generate dozens of files at once
✅ **Consistency**: Enforce naming, structure, parameter conventions
✅ **Testing**: Automatically verify output
✅ **Algorithmic Composition**: Create using rules and patterns

### Disadvantages

❌ **Learning Curve**: Must learn Radiant Voices API
❌ **Abstraction**: One layer removed from actual modules
❌ **Debugging**: Harder to visualize during creation
❌ **Limited Coverage**: Not all SunVox features exposed via API
❌ **Documentation Gaps**: API less documented than SunVox itself

## The Stack

### Radiant Voices

**What it is**: A Python library for creating, reading, modifying, and writing SunVox files.

**Key Features**:
- Nearly 100% coverage of SunVox data structures
- "Pythonic" API (intuitive, follows Python conventions)
- Read and write `.sunvox` and `.sunsynth` files
- SunVox 2.x compatible (version 2.0.0.2.1.2.1)

**Installation**:
```bash
pip install radiant-voices
```

**GitHub**: https://github.com/metrasynth/radiant-voices
**Docs**: https://radiant-voices.readthedocs.io/

### Python

All generation scripts use Python 3.11+. Python provides:
- Easy scripting
- Good string handling (for names, paths)
- Math libraries (for algorithmic composition)
- File I/O

## Basic Structure: Hello World

### Minimal SunVox File

```python
from rv.api import Project, m

# Create empty project
p = Project()
p.name = "Hello SunVox"

# Add a generator
gen = p.new_module(
    m.Generator,
    name="Test Generator",
    x=256,
    y=256
)

# Connect to output
gen >> p.output

# Write to file
with open('hello.sunvox', 'wb') as f:
    p.write_to(f)
```

This creates a valid `.sunvox` file with one generator module.

### Key Components

#### 1. Project
```python
from rv.api import Project

p = Project()
p.name = "My Project"
p.initial_bpm = 125
p.initial_tpl = 6  # Ticks per line
```

The `Project` object represents the entire `.sunvox` file.

#### 2. Modules
```python
from rv.api import m

# Create various module types
kick = p.new_module(m.Kicker, name="Kick", x=256, y=128)
gen = p.new_module(m.Generator, waveform=m.Generator.Waveform.sine)
comp = p.new_module(m.Compressor, threshold=180)
```

Modules are created with `p.new_module(ModuleClass, **parameters)`.

#### 3. Connections
```python
# Connect modules (audio routing)
kick >> compressor >> eq >> p.output

# Multiple inputs to one output
bass >> mixer
chords >> mixer
mixer >> p.output

# Connect to multiple outputs
source >> effect1
source >> effect2  # Parallel processing
```

The `>>` operator connects modules (audio flows left to right).

#### 4. Patterns
```python
from rv.api import Pattern, NOTE, NOTECMD

# Create pattern
pattern = Pattern(name="Kick Pattern", lines=32, tracks=1)

# Add notes
pattern.data[0][0].note = NOTE.C5
pattern.data[0][0].vel = 120
pattern.data[0][0].module = kick.index + 1

# Add note-off
pattern.data[30][0].note = NOTECMD.NOTE_OFF
pattern.data[30][0].module = kick.index + 1

# Attach to project
p.attach_pattern(pattern)
```

Patterns contain note data, accessed via `pattern.data[line][track]`.

#### 5. Writing
```python
# Write to file
with open('output.sunvox', 'wb') as f:
    p.write_to(f)
```

Always open files in **binary mode** (`'wb'`).

## Module Types

Radiant Voices supports all major SunVox modules:

### Generators (Sound Sources)

```python
from rv.api import m

# Analog Generator
analog = p.new_module(
    m.AnalogGenerator,
    waveform=m.AnalogGenerator.Waveform.saw,  # sine, square, saw, triangle, noise
    volume=200,
    attack=10,
    release=150,
    sustain=True,
    filter=m.AnalogGenerator.Filter.lp_12db,  # Low-pass 12dB
    filter_cutoff=180
)

# FM Synth
fm = p.new_module(
    m.Fm,
    c_volume=180,      # Carrier volume
    m_volume=100,      # Modulator volume
    c_freq_ratio=1,    # Carrier frequency ratio (0-16)
    m_freq_ratio=2     # Modulator frequency ratio (0-16)
)

# Sampler
sampler = p.new_module(
    m.Sampler,
    sample_path="/path/to/sample.wav"  # Load external sample
)

# Kicker (kick drum synthesizer)
kick = p.new_module(
    m.Kicker,
    vol=256,
    boost=200,
    release=100
)

# DrumSynth (percussion synthesizer)
drums = p.new_module(
    m.DrumSynth,
    bass_volume=200,   # Kick volume
    hihat_volume=180,  # Hi-hat volume
    snare_volume=150   # Snare volume
)

# Generator (basic oscillator)
gen = p.new_module(
    m.Generator,
    waveform=m.Generator.Waveform.square,
    duty_cycle=128  # Pulse width (0-256)
)
```

### Effects (Audio Processors)

```python
# Compressor
comp = p.new_module(
    m.Compressor,
    volume=256,
    threshold=180,      # 0-256 (lower = more compression)
    slope=0,            # 0=fast, 1=normal
    attack=5,
    release=100,
    mode=m.Compressor.Mode.peak  # or .rms
)

# Filter
filt = p.new_module(
    m.Filter,
    type=m.Filter.Type.lp,  # lp, hp, bp, notch
    freq=150,               # Cutoff frequency
    resonance=100
)

# Delay
delay = p.new_module(
    m.Delay,
    delay_l=6,  # Left delay (0-256)
    delay_r=6,  # Right delay
    channels=m.Delay.Channels.stereo  # mono, stereo
)

# Reverb
reverb = p.new_module(
    m.Reverb,
    volume=256,
    dryout=200,  # Dry signal level
    wetout=100   # Wet signal level
)

# EQ
eq = p.new_module(
    m.Eq,
    low=120,   # Low band (0-256)
    middle=100,
    high=110
)

# Distortion
dist = p.new_module(
    m.Distortion,
    volume=256,
    type=m.Distortion.Type.clipping,  # or .foldback, .saturation
    power=80  # Distortion amount
)

# Amplifier
amp = p.new_module(
    m.Amplifier,
    volume=200,
    inverse=False  # True = phase invert
)
```

### Utility Modules

```python
# Sound2Ctl (convert audio to control signal)
s2c = p.new_module(
    m.Sound2Ctl,
    absolute=True,   # Output absolute values
    gain=180,        # Sensitivity
    smooth=20        # Smoothing amount
)

# LFO (Low Frequency Oscillator)
lfo = p.new_module(
    m.Lfo,
    waveform=m.Lfo.Waveform.sine,  # sine, saw, square, random
    freq=64,         # Frequency
    generator=False  # False = modulator, True = audio rate
)

# MultiSynth (polyphonic container)
multisynth = p.new_module(
    m.MultiSynth,
    transpose=0
)

# MetaModule (load external .sunvox files)
# Note: Cannot load external files programmatically in Radiant Voices
# Must be done manually in SunVox GUI
```

## Parameter Ranges

SunVox parameters typically use specific ranges:

- **Volume/Levels**: 0-256 (256 = 100%, 0 = silence)
- **Filters/Frequencies**: 0-256 (often logarithmic mapping)
- **Time Parameters**: Varies by module (attack, release, etc.)
- **Boolean Options**: True/False or specific enums
- **Ratios**: Often 0-16 range (for FM ratios, etc.)

**Important**: Check valid ranges! Out-of-range values cause errors.

```python
# ✅ Valid
bass = p.new_module(m.AnalogGenerator, release=200)  # 0-256 range

# ❌ Invalid
bass = p.new_module(m.AnalogGenerator, release=512)  # Out of range!
# Error: ControllerValueError: release=512 is not within [0, 256]
```

## Enum Values

Many parameters use enums. **Use lowercase**:

```python
# ✅ Correct
gen = p.new_module(
    m.Generator,
    waveform=m.Generator.Waveform.sine  # lowercase
)

# ❌ Wrong
gen = p.new_module(
    m.Generator,
    waveform=m.Generator.Waveform.SINE  # UPPERCASE doesn't exist
)
```

Common enums:
- Waveforms: `.sine`, `.square`, `.saw`, `.triangle`, `.noise`
- Filter types: `.lp`, `.hp`, `.bp`, `.notch`
- Modes: `.peak`, `.rms`, `.stereo`, `.mono`

## Pattern Creation

Patterns are the most complex part:

### Creating Pattern

```python
from rv.api import Pattern

# Pattern(name, lines, tracks)
pattern = Pattern(
    name="My Pattern",
    lines=32,   # Length in lines (rows)
    tracks=4    # Number of tracks (columns)
)

# Attach to project
p.attach_pattern(pattern)
```

### Adding Notes

```python
from rv.api import NOTE, NOTECMD

# Set note data
line = 0   # Line number (row)
track = 0  # Track number (column)

pattern.data[line][track].note = NOTE.C5
pattern.data[line][track].vel = 120          # Velocity (0-129)
pattern.data[line][track].module = kick.index + 1  # Module to trigger

# Note off
pattern.data[30][track].note = NOTECMD.NOTE_OFF
pattern.data[30][track].module = kick.index + 1
```

### Available Notes

```python
# Chromatic scale
NOTE.C0, NOTE.Cs0, NOTE.D0, NOTE.Ds0, NOTE.E0, NOTE.F0, ...
NOTE.C5, NOTE.Cs5, NOTE.D5, NOTE.Ds5, NOTE.E5, NOTE.F5, ...
NOTE.C9  # Up to C9

# Note commands
NOTECMD.NOTE_OFF     # Stop note
NOTECMD.ALL_NOTES_OFF
NOTECMD.CLEAN_SYNTHS
NOTECMD.STOP
NOTECMD.PLAY
NOTECMD.SET_PITCH
```

### Pattern with Chords

```python
# Create 3-track pattern for chord
chord_pattern = Pattern(name="Am Chord", lines=32, tracks=3)
p.attach_pattern(chord_pattern)

# Track 0: A note
chord_pattern.data[0][0].note = NOTE.A3
chord_pattern.data[0][0].vel = 80
chord_pattern.data[0][0].module = synth.index + 1

# Track 1: C note
chord_pattern.data[0][1].note = NOTE.C4
chord_pattern.data[0][1].vel = 75
chord_pattern.data[0][1].module = synth.index + 1

# Track 2: E note
chord_pattern.data[0][2].note = NOTE.E4
chord_pattern.data[0][2].vel = 75
chord_pattern.data[0][2].module = synth.index + 1
```

### Pattern with Sequence

```python
# Kick pattern (four-on-the-floor)
kick_pattern = Pattern(name="Kick", lines=32, tracks=1)
p.attach_pattern(kick_pattern)

# Every 8 lines (quarter note at 6 TPL)
for line in [0, 8, 16, 24]:
    kick_pattern.data[line][0].note = NOTE.C5
    kick_pattern.data[line][0].vel = 120
    kick_pattern.data[line][0].module = kick.index + 1
```

## Module Positioning

Modules have X/Y coordinates for layout:

```python
# Position modules in a grid
kick = p.new_module(m.Kicker, x=256, y=128)
bass = p.new_module(m.AnalogGenerator, x=256, y=256)
chords = p.new_module(m.Fm, x=256, y=384)

# Horizontal chain
source = p.new_module(m.Generator, x=200, y=256)
effect1 = p.new_module(m.Compressor, x=350, y=256)
effect2 = p.new_module(m.Reverb, x=500, y=256)
```

**Coordinates**:
- Origin (0, 0) is top-left
- X increases rightward
- Y increases downward
- Output module is at `p.output.x, p.output.y`

## Colors

Modules can have custom colors:

```python
kick = p.new_module(
    m.Kicker,
    color=(255, 80, 80)  # RGB tuple (red kick)
)

bass = p.new_module(
    m.AnalogGenerator,
    color=(80, 120, 255)  # Blue bass
)
```

RGB values: 0-255 for each channel.

## Project Properties

```python
p = Project()

# Basic properties
p.name = "My Track"
p.initial_bpm = 125
p.initial_tpl = 6

# Version (for compatibility)
p.sunvox_version = (2, 1, 2, 1)  # SunVox 2.1.2
p.based_on_version = (2, 1, 2, 1)

# Other properties
p.global_volume = 256
p.modules_scale = 256
p.modules_zoom = 256
```

## Complete Example: Basic Track Generator

```python
#!/usr/bin/env python3
from rv.api import Project, Pattern, m, NOTE, NOTECMD

# Create project
p = Project()
p.name = "Generated Track"
p.initial_bpm = 125

# Create kick
kick = p.new_module(
    m.Kicker,
    name="Kick",
    vol=256,
    boost=200,
    x=256,
    y=200,
    color=(255, 100, 100)
)

# Create bass
bass = p.new_module(
    m.AnalogGenerator,
    name="Bass",
    waveform=m.AnalogGenerator.Waveform.sin,
    volume=220,
    attack=5,
    release=150,
    sustain=True,
    x=256,
    y=300,
    color=(100, 150, 255)
)

# Create compressor
comp = p.new_module(
    m.Compressor,
    name="Glue",
    threshold=200,
    slope=0,
    attack=10,
    release=150,
    x=450,
    y=250,
    color=(255, 255, 150)
)

# Connect
kick >> comp >> p.output
bass >> comp

# Create kick pattern
kick_pat = Pattern(name="Kick", lines=32, tracks=1)
p.attach_pattern(kick_pat)
for line in [0, 8, 16, 24]:
    kick_pat.data[line][0].note = NOTE.C5
    kick_pat.data[line][0].vel = 120
    kick_pat.data[line][0].module = kick.index + 1

# Create bass pattern
bass_pat = Pattern(name="Bass", lines=32, tracks=1)
p.attach_pattern(bass_pat)
bass_pat.data[0][0].note = NOTE.A2
bass_pat.data[0][0].vel = 100
bass_pat.data[0][0].module = bass.index + 1
bass_pat.data[30][0].note = NOTECMD.NOTE_OFF
bass_pat.data[30][0].module = bass.index + 1

# Write
with open('generated_track.sunvox', 'wb') as f:
    p.write_to(f)

print("✓ Created generated_track.sunvox")
```

## Reading Existing Files

You can also read and modify existing files:

```python
import rv.api

# Read file
p = rv.api.read_sunvox_file("existing.sunvox")

# Inspect
print(f"Project: {p.name}")
print(f"BPM: {p.initial_bpm}")
print(f"Modules: {len([m for m in p.modules if m is not None])}")

# Modify
p.initial_bpm = 140

# Write back
with open("modified.sunvox", 'wb') as f:
    p.write_to(f)
```

## Common Patterns

### Pattern 1: Algorithmic Composition

```python
import random

# Generate random melody
melody_pattern = Pattern(name="Random Melody", lines=64, tracks=1)
p.attach_pattern(melody_pattern)

scale = [NOTE.C4, NOTE.D4, NOTE.E4, NOTE.G4, NOTE.A4]  # C major pentatonic

for line in range(0, 64, 4):
    note = random.choice(scale)
    vel = random.randint(80, 120)

    melody_pattern.data[line][0].note = note
    melody_pattern.data[line][0].vel = vel
    melody_pattern.data[line][0].module = synth.index + 1
```

### Pattern 2: Parameterized Generation

```python
def create_kick(boost_level):
    """Create kick with variable boost"""
    return p.new_module(
        m.Kicker,
        name=f"Kick Boost {boost_level}",
        boost=boost_level
    )

# Generate variations
light_kick = create_kick(100)
medium_kick = create_kick(200)
heavy_kick = create_kick(256)
```

### Pattern 3: Batch Creation

```python
# Create 10 variations
for i in range(10):
    p = Project()
    p.name = f"Variation {i}"
    p.initial_bpm = 120 + (i * 5)  # 120, 125, 130, ...

    # Add modules...

    with open(f"variation_{i:02d}.sunvox", 'wb') as f:
        p.write_to(f)
```

### Pattern 4: Template System

```python
def create_template(genre):
    """Create genre-specific template"""
    p = Project()

    if genre == "house":
        p.initial_bpm = 125
        # Add house-specific modules
    elif genre == "techno":
        p.initial_bpm = 135
        # Add techno-specific modules

    return p

house_project = create_template("house")
techno_project = create_template("techno")
```

## Debugging

### Common Errors

**1. Range Validation Error**
```
ControllerValueError: release=512 is not within [0, 256]
```
**Solution**: Check parameter ranges, use values within valid bounds.

**2. AttributeError on Enum**
```
AttributeError: SAW. Did you mean: 'saw'?
```
**Solution**: Use lowercase enum values: `.saw` not `.SAW`.

**3. Module Index Error**
```
pattern.data[0][0].module = kick.index  # Wrong!
pattern.data[0][0].module = kick.index + 1  # Correct!
```
**Solution**: Module indices in patterns are 1-based, not 0-based.

### Validation

```python
# Verify file is readable
try:
    p = rv.api.read_sunvox_file("output.sunvox")
    print(f"✓ File valid: {p.name}")
    print(f"  Modules: {len([m for m in p.modules if m is not None])}")
    print(f"  Patterns: {len(p.patterns)}")
except Exception as e:
    print(f"✗ File invalid: {e}")
```

## Limitations

### What Radiant Voices CAN'T Do

❌ **Load external .sunvox as MetaModules** (must do manually in SunVox)
❌ **Access module-specific features** not in API (some obscure parameters)
❌ **Generate automation curves** (controller automation over time)
❌ **Timeline/arrangement editing** (pattern placement in timeline)
❌ **Some effect-specific features** (depends on module)

### Workarounds

- **MetaModules**: Create placeholder modules with instructions to load manually
- **Automation**: Use patterns with controller events
- **Timeline**: Document arrangement in comments/README
- **Missing features**: Create base file in SunVox, load and modify with Radiant Voices

## Files Generated in This Repository

All the following were generated programmatically:

### Sidechain Compression Tutorial
- `8--Techniques/Sidechain-Compression/*.sunvox` (6 files)
- Generated by: `generate_examples.py`
- Demonstrates: Kick→Sound2Ctl→Compressor chains

### Basic House Track
- `basic_house_track.sunvox`
- Generated by: `basic_house_track.py`
- Demonstrates: Full track with drums, bass, chords, lead

### Modular Construction
- `modular_construction/layer1_*.sunvox` (4 files)
- `modular_construction/layer2_*.sunvox` (2 files)
- `modular_construction/layer3_*.sunvox` (1 file)
- Generated by: `create_modular_construction.py`
- Demonstrates: Hierarchical composition

## Best Practices

### 1. Use Functions for Reusability

```python
def create_processed_kick(boost=200, comp_threshold=170):
    kick = p.new_module(m.Kicker, boost=boost)
    comp = p.new_module(m.Compressor, threshold=comp_threshold)
    kick >> comp
    return comp  # Return the output module
```

### 2. Document Parameters

```python
# Create kick with:
# - 200 boost for punch
# - Centered position
# - Red color for visual identification
kick = p.new_module(
    m.Kicker,
    boost=200,    # Punch level
    x=256, y=200,  # Position
    color=(255, 80, 80)  # Red
)
```

### 3. Validate Output

```python
# Always verify file after creation
p_verify = rv.api.read_sunvox_file(output_path)
assert p_verify.name == "Expected Name"
assert len(p_verify.modules) == expected_count
print("✓ Validation passed")
```

### 4. Use Descriptive Names

```python
# ❌ Bad
m1 = p.new_module(m.Kicker)
m2 = p.new_module(m.Compressor)

# ✅ Good
kick = p.new_module(m.Kicker, name="Kick")
kick_comp = p.new_module(m.Compressor, name="Kick Comp")
```

### 5. Organize Large Projects

```python
# Separate concerns
def create_drums():
    kick = p.new_module(m.Kicker, x=256, y=128)
    # ... more drums
    return kick

def create_bass():
    bass = p.new_module(m.AnalogGenerator, x=256, y=256)
    # ... bass chain
    return bass

def create_master():
    master = p.new_module(m.Compressor, x=640, y=300)
    return master

# Build project
drums = create_drums()
bass = create_bass()
master = create_master()

drums >> master >> p.output
bass >> master
```

## Resources

### Radiant Voices
- **GitHub**: https://github.com/metrasynth/radiant-voices
- **Docs**: https://radiant-voices.readthedocs.io/
- **PyPI**: https://pypi.org/project/radiant-voices/

### SunVox
- **Manual**: https://warmplace.ru/soft/sunvox/manual.php
- **Library**: https://warmplace.ru/soft/sunvox/sunvox_lib.php

### Examples
- All generation scripts in this repository
- Radiant Voices examples folder
- SunVox forum: https://warmplace.ru/forum/

## Conclusion

Programmatic SunVox file generation enables:

✅ **Reproducible creation** - Same script → same result
✅ **Algorithmic composition** - Generate from rules
✅ **Batch processing** - Create many variations
✅ **Version control** - Track changes in code
✅ **Documentation** - Code explains structure
✅ **Parameterization** - Easy to modify and experiment

Combined with manual SunVox editing, this provides a powerful hybrid workflow:
- Generate base structures programmatically
- Refine and arrange manually in SunVox
- Export final versions

This is the foundation for **generative music systems**, **algorithmic composition**, and **scalable sound design**.

---

_Know the smallest things and the biggest things, the shallowest things and the deepest things._

_- Miyamoto Musashi_

[(Sitemap)](Sitemap.md)
