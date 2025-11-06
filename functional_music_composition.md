# Functional Music Composition in SunVox

_When you have attained the Way of strategy there will be nothing that you cannot understand._

_- Miyamoto Musashi_

## Overview

While SunVox's MetaModule system enables object-oriented patterns, its **copy-based instantiation model** and **signal flow architecture** actually align closely with **functional programming** paradigms. This document explores how functional programming concepts apply to music composition in SunVox.

## Core Functional Programming Concepts

### 1. Immutability

**In FP**: Data cannot be changed after creation. You create new data instead of modifying existing data.

**In SunVox**:
- Once a `.sunvox` file is loaded as a MetaModule, it becomes **frozen** in the parent project
- Changes to the source file don't affect the loaded instance
- To "update" a MetaModule, you must delete and reload it (creating a new immutable copy)

```
// Functional Programming
const originalArray = [1, 2, 3];
const newArray = [...originalArray, 4];  // Create new, don't mutate

// SunVox Equivalent
original_module.sunvox  → [Load as MetaModule] → Immutable copy in project
modified_module.sunvox  → [Load as MetaModule] → New immutable copy
```

**Benefits**:
- Projects are stable and reproducible
- No "spooky action at a distance" from external changes
- Easy to reason about project state

### 2. Pure Functions

**In FP**: Functions with no side effects. Same input always produces same output.

**In SunVox**:
- A module with fixed parameters is a **pure function**
- Given the same MIDI input, it produces the same audio output
- No hidden state changes

```
// Pure Function
function multiplyByTwo(x) {
    return x * 2;  // No side effects, deterministic
}

// SunVox Pure Module
[MIDI Note C5 @ velocity 100]
    → [Kick Module with fixed parameters]
    → [Identical audio output every time]
```

**Impure Modules**:
- Modules with randomization (Random, Noise)
- Modules affected by external timing (LFO not synced to tempo)
- Sample playback with random start positions

**Making Modules Pure**:
- Fix all parameters (no LFO modulation)
- Sync timing to project BPM
- Set random seed if available
- Disable any external inputs

### 3. First-Class Functions

**In FP**: Functions can be passed as arguments, returned from functions, assigned to variables.

**In SunVox**:
- `.sunvox` files are **first-class citizens**
- Can be loaded into any MetaModule
- Can be passed between projects
- Can be returned from generation scripts

```python
# First-class functions
def apply_effect(sound_function, effect_function):
    return lambda input: effect_function(sound_function(input))

# SunVox equivalent
def apply_effect(sound_module_path, effect_module_path):
    """Load sound module, wrap with effect module"""
    # Returns a new .sunvox file with both combined
    return composite_module.sunvox
```

### 4. Higher-Order Functions

**In FP**: Functions that take functions as arguments or return functions.

**In SunVox**: Modules that process other modules' outputs.

```
// Higher-order function
function mapArray(fn, array) {
    return array.map(fn);
}

// SunVox higher-order module
[MultiSynth Module]
  ├── Synth 1 (input function)
  ├── Synth 2 (input function)
  └── Output: Combined result
```

The MultiSynth is a higher-order module - it takes multiple "sound functions" and combines them.

### 5. Function Composition

**In FP**: Combine simple functions to build complex ones.

```javascript
const compose = (f, g) => x => f(g(x));
const addOne = x => x + 1;
const double = x => x * 2;
const addOneThenDouble = compose(double, addOne);
```

**In SunVox**: Chain modules in series.

```
[Input] → [Module A] → [Module B] → [Module C] → [Output]

         f1          f2          f3
Audio = f3(f2(f1(input)))
```

This is **function composition**! Each module is a function that transforms audio.

**Example**:
```
kick_sound = generate_kick()
compressed = compress(kick_sound)
eq'd = eq(compressed)
final = reverb(eq'd)

// Composed:
final = reverb(eq(compress(generate_kick())))

// In SunVox module chain:
[Kicker] → [Compressor] → [EQ] → [Reverb] → [Output]
```

### 6. Currying & Partial Application

**In FP**: Transform a function with multiple parameters into a series of single-parameter functions.

```javascript
// Currying
const add = a => b => a + b;
const addFive = add(5);  // Partially applied
addFive(3);  // Returns 8
```

**In SunVox**: Pre-configure modules with some parameters set.

```
generic_filter.sunvox (takes frequency, resonance, input)
    ↓ Set frequency to 500Hz, resonance to 80
lowpass_500hz.sunvox (only needs input)
    ↓ Partially applied filter
```

**Practical Use**:
1. Create generic modules with many parameters
2. Save variants with some parameters pre-set
3. Reduces complexity for end users

### 7. Recursion

**In FP**: Functions that call themselves.

**In SunVox**: Feedback loops!

```
// Recursive function
function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

// SunVox recursive signal
[Delay] → [Filter] → [Feedback Module] → back to [Delay]
```

The Feedback module enables recursive audio processing.

**Use Cases**:
- Echo/delay effects
- Resonant filters
- Karplus-Strong synthesis
- Feedback distortion

**Termination Condition**: Decay/attenuation ensures signal eventually stops (like base case in recursion).

### 8. Lazy Evaluation

**In FP**: Compute values only when needed.

**In SunVox**:
- Modules only process when they receive input
- Patterns only play when triggered
- MetaModules only execute when activated

```python
# Lazy evaluation
def expensive_computation():
    return sum(range(1000000))

lazy_value = lambda: expensive_computation()  # Not computed yet
result = lazy_value()  # Computed now when called

# SunVox equivalent
module_in_project.sunvox  # Exists but not computing
[User triggers pattern]    # Now it computes
```

### 9. Map, Filter, Reduce

These fundamental FP operations have SunVox equivalents:

#### Map: Transform each element

```python
# Map in FP
numbers = [1, 2, 3]
doubled = map(lambda x: x * 2, numbers)  # [2, 4, 6]
```

```
# SunVox equivalent: Process multiple notes
Pattern: [C5, E5, G5]
    ↓ [Amplifier +6dB]  (maps each note through same transformation)
Output: [Louder C5, Louder E5, Louder G5]
```

#### Filter: Select elements matching criteria

```python
# Filter in FP
numbers = [1, 2, 3, 4, 5]
evens = filter(lambda x: x % 2 == 0, numbers)  # [2, 4]
```

```
# SunVox equivalent: Filter module
Audio with frequencies [100Hz, 500Hz, 2000Hz]
    ↓ [Low-pass filter @ 1000Hz]
Output: [100Hz, 500Hz] (filtered out 2000Hz)
```

#### Reduce: Combine elements into single value

```python
# Reduce in FP
numbers = [1, 2, 3, 4]
sum = reduce(lambda acc, x: acc + x, numbers)  # 10
```

```
# SunVox equivalent: Mixer/Amplifier
Multiple audio streams [stream1, stream2, stream3]
    ↓ [Amplifier/Mixer]
Output: Single mixed stream
```

## Functional Architectures in SunVox

### Pipeline Architecture

Data flows through a series of transformations:

```
Input → Transform1 → Transform2 → Transform3 → Output
```

Each module is a pure transformation function.

**Example: Drum Processing Pipeline**
```
[Raw Kick Sample]
    → [Compressor]      (dynamics transformation)
    → [EQ]              (frequency transformation)
    → [Saturation]      (harmonics transformation)
    → [Limiter]         (peak transformation)
    → [Output]
```

### Parallel Processing (Applicative Functors)

Process multiple streams independently then combine:

```
       ┌→ [Process A] ┐
Input ─┼→ [Process B] ┼→ Combine → Output
       └→ [Process C] ┘
```

**Example: Multi-band Processing**
```
                  ┌→ [Low-pass] → [Bass Comp] ┐
[Full Spectrum] ──┼→ [Band-pass] → [Mid EQ]   ┼→ [Mixer] → Output
                  └→ [High-pass] → [Hi Excite]┘
```

Each band is processed by a pure function, results combined.

### Functor Pattern

A context that can be mapped over:

```haskell
-- In Haskell
fmap :: (a -> b) -> f a -> f b

-- Example
fmap (+1) (Just 5)  -- Just 6
```

**In SunVox**: A pattern containing notes is a functor.

```
Pattern = [C5, E5, G5]  -- Functor containing notes

Transpose = fmap (+12)  -- Map function (add 12 semitones)

Result = [C6, E6, G6]   -- Mapped functor
```

### Monad Pattern (Sequential Context)

Monads handle sequential operations with context:

```haskell
-- In Haskell
(>>=) :: m a -> (a -> m b) -> m b  -- "bind" operator
```

**In SunVox**: Pattern sequencing is monadic!

```
Pattern 1 >>= (result triggers) Pattern 2 >>= Pattern 3

Timeline:
[Pattern A] → finish → [Pattern B] → finish → [Pattern C]
```

Each pattern's completion triggers the next, maintaining temporal context.

## Functional Design Patterns

### 1. Immutable Data Flow

**Never modify signals in place; always create new transformed versions.**

```
❌ BAD (mutable):
audio_buffer.modify(add_reverb)  // Mutates original

✅ GOOD (immutable):
dry_signal → [Reverb Module] → wet_signal  // Creates new signal
```

**Implementation**:
- Use parallel signal paths for wet/dry
- Create new modules rather than modifying existing
- Save variations as new files

### 2. Point-Free Style

**Define transformations without mentioning the data being transformed.**

```javascript
// Point-free in FP (no mention of 'x')
const double = x => x * 2;
const addOne = x => x + 1;
const doubleThenAddOne = compose(addOne, double);  // No 'x' mentioned

// SunVox point-free
[Input] → [Effect Chain] → [Output]
// The chain is defined without mentioning specific audio data
```

### 3. Function Memoization

**Cache results of expensive pure functions.**

**In SunVox**:
- Render complex modules to samples
- Reuse rendered audio instead of recomputing
- Bounce-to-audio workflow

```
Expensive: [Complex FM Synth] → [Heavy Reverb] → [Convolution]
Memoized:  [Sampler with pre-rendered result]
```

### 4. Referential Transparency

**Expressions can be replaced with their values without changing program behavior.**

```javascript
// Referentially transparent
const x = 5;
const y = x + 3;  // Can replace 'x' with '5'
const y = 5 + 3;  // Same result
```

**In SunVox**: Pure modules are referentially transparent.

```
[Kick Module @ C5] → [Audio Output X]
// Any kick module producing X can be swapped
[Different Kick @ C5] → [Same Audio Output X]
```

This enables A/B testing and modular swapping.

### 5. Closure Pattern

**Functions that capture their environment.**

```javascript
function makeMultiplier(factor) {
    return function(x) {
        return x * factor;  // Captures 'factor'
    };
}
const double = makeMultiplier(2);
```

**In SunVox**: Modules with "baked-in" parameters.

```
generic_compressor.sunvox (ratio, threshold, attack, release)
    ↓ Set ratio=4:1, threshold=-20dB
vocal_compressor.sunvox  // Captures those parameters
```

The vocal compressor is a "closure" over the generic compressor with captured settings.

## Functional Workflows

### Workflow 1: Composition Pipeline

Build tracks by composing pure transformations:

```python
# Pseudocode
kick = generate_kick()
compressed_kick = compress(kick)
eq_kick = eq(compressed_kick)
final_kick = reverb(eq_kick)

bass = generate_bass()
filtered_bass = filter(bass)

mix = combine(final_kick, filtered_bass)
master = master_chain(mix)
```

**In SunVox**:
1. Create pure generator modules (kick, bass)
2. Create pure effect modules (compress, eq, reverb)
3. Compose them in series
4. Save each composition stage as a module
5. Final track is composition of all stages

### Workflow 2: Parallel Processing

Process independent streams then merge:

```python
# Parallel processing
def process_track(audio):
    low = low_pass(audio) |> compress |> eq_low
    mid = mid_pass(audio) |> excite |> eq_mid
    high = high_pass(audio) |> shimmer |> eq_high
    return mix([low, mid, high])
```

**In SunVox**:
1. Split signal to multiple paths (MultiSynth or parallel sends)
2. Apply pure transformations to each
3. Recombine at mixer
4. All paths are independent (functional purity)

### Workflow 3: Lazy Generation

Generate elements only when needed:

```python
# Lazy sequence
def infinite_beats():
    i = 0
    while True:
        yield generate_beat(i)
        i += 1

# Take only what you need
first_8_beats = take(8, infinite_beats())
```

**In SunVox**:
1. Create pattern with many possible variations
2. Only render/play when triggered
3. Use pattern effects to generate variations on the fly
4. MetaModules compute only when receiving input

### Workflow 4: Fold/Reduce Pattern

Build up complexity by folding transformations:

```python
# Fold in FP
effects = [reverb, delay, chorus, eq]
processed = fold(lambda audio, effect: effect(audio), dry_signal, effects)
```

**In SunVox**:
1. Start with dry signal
2. Apply first effect → intermediate result
3. Apply second effect to intermediate → new intermediate
4. Continue folding until final result
5. Each step is pure transformation

## Functional vs. Object-Oriented: When to Use Each

### Use Functional Approach When:

✅ **Building effect chains** (composition pipelines)
✅ **Processing stems** (map/filter/reduce operations)
✅ **Creating reusable processors** (pure functions)
✅ **Ensuring reproducibility** (same input → same output)
✅ **Parallel processing** (independent streams)
✅ **Algorithmic composition** (generating from rules)

### Use Object-Oriented Approach When:

✅ **Building instrument libraries** (encapsulated state)
✅ **Creating templates** (reusable starting points)
✅ **Organizing complex projects** (hierarchical structure)
✅ **Team collaboration** (component ownership)
✅ **Version management** (tracking iterations)

### Hybrid Approach (Best of Both)

Most real-world projects benefit from combining paradigms:

```
OOP: Organize project structure
  ├── Layer 1: Instrument objects (kicks, basses, leads)
  ├── Layer 2: Section objects (rhythm, harmony)
  └── Layer 3: Track object (final composition)

FP: Process audio within each layer
  ├── Pure signal chains (compress → eq → reverb)
  ├── Immutable transformations (no destructive editing)
  └── Composition (build complex from simple)
```

## Advanced Functional Concepts

### Transducers

Composable algorithmic transformations that are independent of input/output sources:

```javascript
// Transducer in JS
const mapping = map(x => x * 2);
const filtering = filter(x => x > 5);
const transducer = compose(filtering, mapping);

// Apply to different sources
transduce(transducer, array);
transduce(transducer, stream);
```

**In SunVox**: Effect chains that work on any input.

```
[Transducer Module Chain]
  Normalize → Compress → EQ → Saturate

Can accept:
- Kick drum
- Bass line
- Vocal
- Full mix
```

The chain is defined independent of source.

### Lenses

Functional way to focus on and update nested data:

```javascript
// Lens in FP
const volumeLens = lens(
    obj => obj.volume,           // getter
    (val, obj) => ({...obj, volume: val})  // setter
);

const module = {name: "Kick", volume: 0.8};
const louder = set(volumeLens, 1.0, module);
```

**In SunVox**: Controller mappings are lenses!

- Focus on specific parameter in nested MetaModule
- Read/write without affecting other parameters
- User-defined controllers expose lenses

### Continuation-Passing Style

Pass "what to do next" as a parameter:

```javascript
// CPS
function add(x, y, cont) {
    cont(x + y);
}

add(3, 4, result => console.log(result));  // 7
```

**In SunVox**: Event chains with note-offs and follow actions.

```
Pattern A plays note
    → On note-off, trigger Pattern B
    → Pattern B plays, triggers Pattern C
    → etc.
```

Each event carries continuation (what happens next).

## Benefits of Functional Approach in SunVox

### 1. Predictability
- Pure modules always produce same output for same input
- Easy to debug and reason about
- No hidden state changes

### 2. Testability
- Test each module independently
- Known inputs → known outputs
- No dependency on external state

### 3. Reusability
- Pure functions compose easily
- Same module works in any context
- No coupling to specific projects

### 4. Parallelization
- Independent processing paths can run concurrently
- No race conditions (immutable data)
- Efficient multi-core rendering

### 5. Reproducibility
- Same project file → identical output every time
- Perfect for archival and redistribution
- No "works on my machine" issues

## Practical Example: Functional Kick Drum Design

```python
# Functional approach to kick design
from rv.api import Project, m

def create_kick_generator():
    """Pure function: No side effects"""
    return m.Kicker(vol=256, boost=200)

def add_compression(module):
    """Pure function: Returns new structure"""
    comp = m.Compressor(threshold=170, ratio=8)
    return connect(module, comp)

def add_eq(module):
    """Pure function: Returns new structure"""
    eq = m.EQ(low=120, mid=100)
    return connect(module, eq)

def add_saturation(module):
    """Pure function: Returns new structure"""
    sat = m.Distortion(type='soft', amount=50)
    return connect(module, sat)

# Compose functions
kick_chain = compose(
    create_kick_generator,
    add_compression,
    add_eq,
    add_saturation
)

# Execute composition
final_kick = kick_chain()  # Pure, repeatable result
```

Every step is a pure function. Same call → same result.

## Conclusion

SunVox's architecture naturally supports functional programming:

- **Immutability**: MetaModules are frozen copies
- **Pure functions**: Modules with fixed parameters
- **Composition**: Chain modules together
- **First-class**: `.sunvox` files as values
- **Lazy evaluation**: Compute only when triggered

The functional paradigm provides:
- ✅ Predictability
- ✅ Reproducibility
- ✅ Testability
- ✅ Composability
- ✅ Parallelization

Combined with OOP patterns for organization, you get a powerful hybrid approach:
- **OOP** for structure and encapsulation
- **FP** for processing and transformation

Both paradigms leverage the same underlying features (MetaModules, signal flow), but emphasize different aspects. Choose the paradigm that fits your workflow, or combine them for maximum power.

## Related Documents

- [Object-Oriented Music Composition](object_oriented_music_composition.md)
- [Generative SunVox](generative_sunvox.md)
- [Modular Construction Demo](modular_construction/README.md)

---

_There is nothing outside of yourself that can ever enable you to get better, stronger, richer, quicker, or smarter. Everything is within._

_- Miyamoto Musashi_

[(Sitemap)](Sitemap.md)
