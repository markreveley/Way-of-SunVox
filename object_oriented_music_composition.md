# Object-Oriented Music Composition in SunVox

_To know ten thousand things, know one well._

_- Miyamoto Musashi_

## Overview

SunVox's MetaModule system enables **object-oriented music composition**, where musical structures can be encapsulated, reused, and composed hierarchically. However, unlike traditional OOP with live references, SunVox uses a **copy-based instantiation model** that has important implications for workflow.

## Core Concepts

### 1. Encapsulation

**Modules as Objects**: Each `.sunvox` file represents a self-contained object with:
- **State**: Module parameters, connections, patterns
- **Behavior**: How it responds to MIDI input or pattern playback
- **Interface**: Input/output connections, exposed controllers

```
[Kick Module Object]
├── Internal State: Kicker parameters, compression settings
├── Behavior: Responds to C5 note with specific sound
└── Interface: Audio output, velocity sensitivity
```

### 2. Composition Over Inheritance

SunVox doesn't support traditional inheritance, but achieves similar goals through **composition**:

```
Rhythm Section (Composite)
├── Kick Module (Component)
├── Hihat Module (Component)
└── Mixer (Aggregator)
```

This is actually closer to **composition patterns** in modern OOP, which are often preferred over inheritance.

### 3. Instantiation Model: Copy vs. Reference

**CRITICAL INSIGHT**: When you load a `.sunvox` file as a MetaModule, SunVox **copies the entire project** into the parent. This is fundamentally different from class instantiation in traditional OOP.

#### Traditional OOP (Reference Model)
```python
class KickDrum:
    def __init__(self):
        self.volume = 100

kick1 = KickDrum()  # Creates reference to class
kick2 = KickDrum()  # Creates another reference

# If class definition changes, both instances use new code
```

#### SunVox MetaModules (Copy Model)
```
[layer1_kick.sunvox file on disk]
    ↓ Load as MetaModule
[Copy embedded in project A]

[layer1_kick.sunvox file on disk]
    ↓ Load as MetaModule
[Copy embedded in project B]

# If you modify layer1_kick.sunvox on disk,
# projects A and B are NOT affected!
```

### Implications of Copy Model

**Advantages:**
- ✅ **Portability**: Projects are self-contained, no broken dependencies
- ✅ **Stability**: External changes can't break existing projects
- ✅ **Independence**: Each instance can be modified without affecting others
- ✅ **No path issues**: Works across different systems/directories

**Disadvantages:**
- ❌ **No propagation**: Bug fixes don't automatically update all uses
- ❌ **File bloat**: Multiple copies increase project size
- ❌ **Version control**: Hard to track which version was used
- ❌ **Updates require manual work**: Must reload MetaModule in each project

### Workflow Implications

This copy model suggests different workflows:

#### ❌ **NOT IDEAL**: "Living Library" Approach
```
1. Build library of modules
2. Use them in 100 projects
3. Fix bug in kick module
4. Expect all 100 projects to automatically update ← DOESN'T WORK
```

#### ✅ **BETTER**: "Template Stamping" Approach
```
1. Build library of modules
2. Use them as STARTING POINTS for projects
3. Each project gets a COPY that can be customized
4. When you need a bug fix, manually update affected projects
```

#### ✅ **BEST**: "Versioned Components" Approach
```
1. Build library with version numbers
   - kick_v1.sunvox
   - kick_v2.sunvox (bug fix)
   - kick_v3.sunvox (new feature)
2. Projects document which versions they use
3. Upgrade projects intentionally, test each time
4. Old projects remain stable with old versions
```

## OOP Patterns in SunVox

### Factory Pattern

Create "factory" projects that generate different variations:

```
kick_factory.sunvox
├── Load different kick samples
├── Apply consistent processing chain
└── Save as kick_808.sunvox, kick_909.sunvox, etc.
```

**Implementation**: Use a template `.sunvox` with processing chain, swap samples, export variations.

### Builder Pattern

Construct complex objects step-by-step:

```
track_builder.sunvox
├── Step 1: Load rhythm section
├── Step 2: Load harmonic section
├── Step 3: Add master effects
└── Step 4: Connect and balance
```

**Implementation**: Layer-by-layer construction as demonstrated in `modular_construction/`.

### Decorator Pattern

Wrap modules with additional behavior:

```
basic_kick.sunvox
    ↓ wrap
[reverb_decorator.sunvox with basic_kick as MetaModule]
    ↓ wrap
[sidechain_decorator.sunvox with reverb_kick as MetaModule]
```

**Implementation**: Create processing shells that load other modules as MetaModules.

### Prototype Pattern

Clone and modify existing instances:

```
1. Load project_template.sunvox
2. Modify patterns/parameters
3. Save as project_variation_1.sunvox
```

**Implementation**: Save template projects, use "Save As" to create variations.

## Architectural Patterns

### Layered Architecture

```
LAYER 4: Application (Full tracks)
LAYER 3: Business Logic (Sections, arrangements)
LAYER 2: Service Layer (Instrument groups)
LAYER 1: Data Layer (Individual modules)
```

Each layer only depends on the layer below.

### Microservices Architecture

Each module is a "microservice":
- Self-contained
- Single responsibility
- Communicates via audio/control signals
- Independently developed and tested

### Event-Driven Architecture

Modules respond to events:
- MIDI notes (triggers)
- Controller changes (parameter updates)
- Pattern events (sequenced actions)

## Object-Oriented Design Principles in SunVox

### SOLID Principles Applied

**Single Responsibility Principle**
- Each module should do ONE thing well
- ✅ Good: `kick.sunvox` just makes kick sounds
- ❌ Bad: `kitchen_sink.sunvox` does drums, bass, chords, and leads

**Open/Closed Principle**
- Open for extension (add effects, layer modules)
- Closed for modification (don't break existing connections)

**Liskov Substitution Principle**
- Any kick module should be swappable with another
- Interface compatibility: all respond to same MIDI notes

**Interface Segregation Principle**
- Expose only necessary controllers
- Don't force users to set 50 parameters if 5 will do

**Dependency Inversion Principle**
- Depend on abstractions (audio signals) not concrete implementations
- High-level sections shouldn't know details of low-level modules

### DRY (Don't Repeat Yourself)

Build reusable modules instead of recreating the same chain in every project:

```
❌ BAD: Recreate "kick → compression → EQ" in 10 projects
✅ GOOD: Create "compressed_kick.sunvox" once, load 10 times
```

### Separation of Concerns

Separate:
- **Sound generation** (oscillators, samples)
- **Sound processing** (effects, filters)
- **Sequencing** (patterns, arrangement)
- **Mixing** (levels, panning, master chain)

## Comparison with Functional Programming

The copy-based instantiation model actually has parallels with **functional programming**:

### Immutability
- Once loaded, MetaModules are "frozen" in the parent
- Changes to source don't affect loaded instances
- Similar to immutable data structures in FP

### Pure Functions
- A `.sunvox` module with patterns is like a pure function:
  - Same input (MIDI notes) → same output (audio)
  - No side effects
  - Deterministic

### Composition
- Combine smaller functions to build larger ones
- `kick ∘ compress ∘ eq = processed_kick`
- This is **function composition**, core to FP

See [Functional Programming Paradigm](functional_music_composition.md) for detailed exploration.

## Practical Workflows

### Workflow 1: Personal Library

**Goal**: Build reusable components for your own projects

1. **Create base library** (Layer 0)
   - Individual modules: kicks, basses, leads
   - Save as `.sunsynth` files

2. **Build combinations** (Layer 1)
   - Combine base modules with effects
   - Save as working `.sunvox` files

3. **Template projects** (Layer 2)
   - Load Layer 1 modules
   - Set up routing and patterns
   - Save as starting points

4. **Active projects** (Layer 3)
   - Copy from Layer 2 templates
   - Customize and develop
   - Accept that changes don't propagate backward

### Workflow 2: Collaborative Production

**Goal**: Multiple producers working together

1. **Component ownership**
   - Producer A: Drums
   - Producer B: Bass & harmony
   - Producer C: Leads & effects

2. **Versioned releases**
   - Each producer exports versions
   - `drums_v1.sunvox`, `drums_v2.sunvox`
   - Main project documents which versions used

3. **Integration testing**
   - Load all components into master project
   - Test combinations
   - Report issues back to component owners

4. **Release freeze**
   - When ready, freeze all versions
   - Main project is locked to those versions
   - Future updates require explicit integration phase

### Workflow 3: Sound Design R&D

**Goal**: Experiment with techniques, build knowledge base

1. **Technique modules**
   - `sidechain_compression_demo.sunvox`
   - `fm_synthesis_demo.sunvox`
   - Each demonstrates ONE concept

2. **Documentation**
   - README for each module
   - Explain parameters, how to use
   - Show variations

3. **Catalog/Index**
   - Master spreadsheet or database
   - Tag by: type, genre, difficulty, uses
   - Quick reference for future projects

4. **Evolution**
   - Improve techniques over time
   - Version each improvement
   - Keep old versions for backwards compatibility

## Advanced Concepts

### Polymorphism via MIDI Mapping

Different modules respond to the same MIDI input differently:

```
MIDI C5 → kick_808.sunvox    → 808-style kick
MIDI C5 → kick_acoustic.sunvox → acoustic kick
MIDI C5 → kick_noise.sunvox   → noise-based kick
```

All three implement the "kick drum interface" but produce different results.

### Abstraction Layers

Hide complexity behind simple interfaces:

```
[User sees: "Epic Bass" module with 5 knobs]
    ↓
[Actually: 15 internal modules with 100+ parameters]
```

MetaModules with user-defined controllers achieve this.

### Dependency Injection

Pass dependencies rather than hard-coding:

```
rhythm_section.sunvox
├── Slot 1: [Load any kick module]
├── Slot 2: [Load any hihat module]
└── Mixer connects automatically
```

This makes rhythm_section reusable with different sounds.

## Limitations & Workarounds

### Limitation 1: No True References

**Problem**: Changes to source modules don't propagate
**Workaround**:
- Version control your module library
- Document dependencies
- Manual update process when needed
- Accept copies as "snapshots in time"

### Limitation 2: No Automatic Updates

**Problem**: Bug fixes require manual work across projects
**Workaround**:
- Test thoroughly before distributing modules
- Batch update related projects together
- Script the update process (open → replace → save)

### Limitation 3: File Size Bloat

**Problem**: Multiple copies increase size
**Workaround**:
- Use `.sunsynth` for smaller components
- Compress project archives
- Accept the tradeoff for portability

### Limitation 4: Version Tracking

**Problem**: Hard to know which module version a project uses
**Workaround**:
- Name modules with versions: `kick_v2.sunvox`
- Document in project notes
- Tag commits in version control

## Conclusion

SunVox's MetaModule system enables powerful object-oriented composition patterns, but with an important caveat: it uses **copy-based instantiation** rather than reference-based. This makes it more like:

- **Prototypal inheritance** (clone and modify)
- **Composition** (assemble from parts)
- **Immutable data structures** (changes don't propagate)

Understanding this model allows you to:
- ✅ Design appropriate workflows
- ✅ Set realistic expectations
- ✅ Leverage the benefits (portability, stability)
- ✅ Mitigate the drawbacks (manual updates, versioning)

The copy model is actually a **feature**, not a bug - it ensures your projects remain stable and portable, trading dynamic updates for reliability.

## Related Documents

- [Functional Music Composition](functional_music_composition.md) - FP paradigm in SunVox
- [Generative SunVox](generative_sunvox.md) - Programmatic generation techniques
- [Modular Construction Demo](modular_construction/README.md) - Practical examples

---

_The way of strategy is the way of nature. When you appreciate the power of nature, knowing rhythm of any situation, you will be able to hit the enemy naturally and strike naturally._

_- Miyamoto Musashi_

[(Sitemap)](Sitemap.md)
