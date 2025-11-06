# Modular SunVox Construction - Hierarchical Composition

_To become the enemy, see yourself as the enemy of the enemy._

_- Miyamoto Musashi_

This demonstration showcases **object-oriented music composition** using SunVox's MetaModule capability, where entire `.sunvox` files can be loaded as modules within other projects.

## Concept: Layered Complexity

Instead of creating one monolithic project, we build complexity in layers:

```
LAYER 1: Simple Building Blocks
  ↓ (combine via MetaModules)
LAYER 2: Combined Sections
  ↓ (combine via MetaModules)
LAYER 3: Final Composition
  ↓ (can go deeper...)
LAYER N: Infinite depth possible
```

## The Files

### 📦 Layer 1 - Building Blocks (4 files)

Individual, self-contained instruments that can be reused across projects:

- **`layer1_kick.sunvox`** - Kick drum with compression
  - Kicker module → Compressor → Output
  - Pattern: Four-on-the-floor

- **`layer1_bass.sunvox`** - Sub bass synth
  - Analog Generator (sine wave) → Filter → Output
  - Pattern: Single A2 note

- **`layer1_chords.sunvox`** - Chord synthesizer
  - FM synth → Reverb → Output
  - Pattern: Am triad (A-C-E)

- **`layer1_hihat.sunvox`** - Hi-hat generator
  - DrumSynth → Output
  - Pattern: 8th note hi-hats

### 🎛️ Layer 2 - Combined Sections (2 files)

Larger functional units that combine Layer 1 modules:

- **`layer2_rhythm_section.sunvox`**
  - Combines: Kick + Hi-Hat
  - Includes: Mixer for balance
  - Use: Complete rhythm foundation

- **`layer2_harmonic_section.sunvox`**
  - Combines: Bass + Chords
  - Includes: Mixer for blend
  - Use: Complete harmonic content

### 🎵 Layer 3 - Final Track (1 file)

The complete composition assembled from Layer 2 sections:

- **`layer3_final_track.sunvox`**
  - Combines: Rhythm Section + Harmonic Section
  - Includes: Master compression
  - Use: Full playable track

## How to Use MetaModules (Manual Steps)

While the files are generated programmatically, **loading them as MetaModules** requires manual steps in SunVox:

### Enhancing Layer 2 Files:

1. Open `layer2_rhythm_section.sunvox` in SunVox
2. Delete the placeholder modules
3. Right-click on empty space → **New** → **MetaModule**
4. In the MetaModule window, click **LOAD**
5. Select `layer1_kick.sunvox`
6. Repeat for hi-hat: Load `layer1_hihat.sunvox` into another MetaModule
7. Connect the MetaModules to the mixer
8. Save the enhanced file

### Enhancing Layer 3 File:

1. Open `layer3_final_track.sunvox`
2. Replace placeholders with MetaModules
3. Load `layer2_rhythm_section.sunvox` into one MetaModule
4. Load `layer2_harmonic_section.sunvox` into another MetaModule
5. Now you have a 3-layer hierarchical composition!

## Benefits of Modular Construction

✅ **Reusability** - Build a library of instruments and sections
✅ **Maintainability** - Fix bugs in one place, all uses update
✅ **Organization** - Complex projects stay manageable
✅ **Collaboration** - Share building blocks with others
✅ **Experimentation** - Easily swap components (try different kicks, etc.)
✅ **Version Control** - Track changes to individual components
✅ **Performance** - Lighter projects when modules are encapsulated

## Workflow Philosophy

This mirrors software engineering best practices:

| Software Concept | SunVox Equivalent |
|-----------------|-------------------|
| Functions | Layer 1 instruments |
| Classes | Layer 2 sections |
| Modules | Layer 3 compositions |
| Libraries | Shared .sunsynth collections |
| Inheritance | MetaModule nesting |
| Composition | Loading modules into projects |

## Going Deeper

You can extend this to any depth:

- **Layer 4**: Multiple tracks combined into an EP
- **Layer 5**: EPs combined into an album
- **Layer 6**: Generative variations of albums
- **Layer N**: Limited only by your imagination

Each layer adds a level of abstraction and reusability.

## Example Use Cases

### 1. Instrument Library
Build a collection of Layer 1 modules:
- Various kick drums (acoustic, 808, 909, etc.)
- Bass synths (sub, acid, reese, etc.)
- Chord machines (piano, strings, pads, etc.)
- Percussion (hats, claps, shakers, etc.)

Save as `.sunsynth` files for cross-project reuse.

### 2. Genre Templates
Create Layer 2 templates for different genres:
- `house_rhythm_section.sunvox` (4/4 kick + hats)
- `dubstep_rhythm_section.sunvox` (half-time + wobble)
- `techno_rhythm_section.sunvox` (minimalist + rolling)

Mix and match with different harmonic sections.

### 3. Stem-Based Composition
Layer 2 files can serve as stems:
- Drums
- Bass
- Chords
- Melody
- FX

Load into Layer 3, arrange, and mix with master effects.

### 4. Collaborative Production
Multiple producers can work on different layers:
- Producer A: Layer 1 sound design
- Producer B: Layer 2 arrangement
- Producer C: Layer 3 mixing/mastering

Each works in their domain, then combines.

## Advanced Techniques

### MetaModule Controller Mapping
MetaModules support up to 96 custom controllers, allowing you to:
- Expose key parameters from inner modules
- Create macro controls for complex patches
- Build custom instruments with unified interfaces

### Pattern Playback vs. Module Selection
MetaModules can operate in two modes:
1. **Module Selection** - Play individual generators inside (polyphonic)
2. **Pattern Playback** - Play the entire inner project (monophonic, but includes sequences)

Choose based on your needs.

### BPM Synchronization
MetaModules automatically sync to parent project BPM, making tempo changes affect all layers simultaneously.

## Related Documentation

- [MetaModule Documentation](../../2--Modules/h--Misc-Modules/MetaModule)
- [Pattern Editing](../../5--Patterns)
- [Project Organization](../../6--Projects)

---

## Generation

All files were **programmatically generated** using the `create_modular_construction.py` script with Radiant Voices library. This ensures reproducibility and demonstrates how modular systems can be built algorithmically.

To regenerate: `python3 create_modular_construction.py`

---

_In strategy it is important to see distant things as if they were close and to take a distanced view of close things._

_- Miyamoto Musashi_

[(Sitemap)](../Sitemap.md)
