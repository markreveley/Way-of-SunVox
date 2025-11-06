_The primary thing when you take a sword in your hands is your intention to cut the enemy, whatever the means. Whenever you parry, hit, spring, strike or touch the enemy's cutting sword, you must cut the enemy in the same movement. It is essential to attain this._

_If you think only of hitting, springing, striking or touching the enemy, you will not be able actually to cut him._

_- Miyamoto Musashi_

# Sidechain Compression

## What is Sidechain Compression?

Sidechain compression (also called "ducking") is a dynamic processing technique where one audio signal controls the compression applied to another signal. The most common use is creating the "pumping" effect in electronic dance music where the bassline ducks in volume every time the kick drum hits, creating rhythmic space and energy.

However, sidechain compression is far more than just an EDM effect. It's a fundamental mixing technique used to:

- **Create space in a mix** - Make room for important elements (like kick drums or vocals) by ducking competing frequencies
- **Add rhythmic movement** - Create pulsing, breathing textures
- **Improve clarity** - Separate instruments occupying similar frequency ranges
- **Control dynamics** - Automatically balance levels between competing elements

## How It Works in SunVox

In SunVox, sidechain compression is achieved by routing a **control signal** (the "key" or "sidechain input") to modulate the parameters of a **Compressor** module affecting a different audio signal.

The basic signal flow:
1. **Trigger Source** (e.g., kick drum) → routes to a controller or Sound2Ctl module
2. **Sound2Ctl** converts the audio amplitude into a control signal
3. **Control Signal** → modulates the Compressor's Threshold or Volume parameters
4. **Target Audio** (e.g., bassline) → passes through the Compressor and gets ducked

---

## Tutorial 1: Classic Kick-to-Bass Sidechain (EDM Pumping)

![](sidechain_basic_setup.gif)

This is the quintessential sidechain compression setup used in house, techno, dubstep, and most electronic music.

### Step-by-Step Instructions:

**1. Create Your Source Sounds**

Create or load:
- A **kick drum** pattern (this will be your trigger)
- A **bassline** or pad that plays sustained notes

**2. Build the Sidechain Signal Chain**

For the bassline/target audio:
1. Create your bass instrument module (e.g., Analog Generator, FM, or Sampler)
2. Add a **Compressor** module after the bass
3. Connect the Compressor to the Output
4. Set the Compressor parameters:
   - **Threshold**: -20 to -30 dB (start here, adjust to taste)
   - **Ratio**: 4:1 to 10:1 (higher = more pronounced ducking)
   - **Attack**: 1-5 ms (fast attack for immediate ducking)
   - **Release**: 50-300 ms (controls how quickly the sound returns - shorter = tighter pumping, longer = smoother)
   - **Slope**: Fast or Normal

**3. Create the Control Signal**

1. Create a **Sound2Ctl** module
2. Connect your **kick drum** output to the Sound2Ctl input (this taps the kick signal without affecting its audio path)
3. Set Sound2Ctl parameters:
   - **Absolute**: ON (ensures positive control values)
   - **Gain**: Adjust to control sensitivity (higher = more pronounced effect)
   - **Smooth**: 0-50 (add smoothing if needed for less abrupt transitions)

**4. Link the Control to the Compressor**

1. In the **Pattern Editor**, select the Compressor module
2. Open the **Controllers** section
3. Create an automation line that links the Sound2Ctl output to either:
   - **Compressor Threshold** (traditional method - lowers threshold when kick hits)
   - OR **Compressor Volume** (alternative - reduces output volume directly)

**5. Fine-Tune the Effect**

Play your pattern and adjust:
- **Sound2Ctl Gain**: How much the kick triggers the compression
- **Compressor Release**: How quickly the bass returns after the kick (this creates the "pump" timing)
- **Compressor Ratio**: How aggressive the ducking is
- If the effect is too subtle, increase the Sound2Ctl gain or lower the Compressor threshold
- If it's too extreme, decrease the ratio or increase the threshold

![](sidechain_compressor_settings.png)

---

## Tutorial 2: Sidechain for Clarity (Vocal-to-Music Ducking)

![](sidechain_vocal_clarity.gif)

This technique creates space for vocals by gently ducking the backing music whenever the vocalist sings.

### Differences from EDM Pumping:

Use much more **subtle settings** for a transparent effect:
- **Compressor Ratio**: 2:1 to 4:1 (gentle)
- **Compressor Attack**: 5-15 ms (slightly slower for smoothness)
- **Compressor Release**: 100-400 ms (longer for natural sound)
- **Sound2Ctl Gain**: Lower values for subtle ducking (you want 2-4 dB of reduction, not 10+ dB)

### Setup:

1. Route the **vocal track** (or a dedicated trigger track following vocal timing) to a Sound2Ctl
2. Connect the Sound2Ctl to modulate a Compressor on the:
   - **Music bus** (all instruments together)
   - OR **Specific competing instruments** (guitars, pads, synths that occupy midrange frequencies)
3. Adjust so the music dips just 2-4 dB when vocals are present
4. The listener shouldn't notice compression - they should just notice the vocal sits perfectly in the mix

---

## Tutorial 3: Rhythmic Gating Effect (Extreme Sidechain)

![](sidechain_rhythmic_gate.gif)

Push sidechain compression to extreme settings to create rhythmic gating effects.

### Settings for Gating:

- **Compressor Ratio**: 10:1 or higher (∞:1 if available)
- **Compressor Threshold**: Very low (-40 to -50 dB)
- **Compressor Attack**: 0-1 ms (instant)
- **Compressor Release**: 10-50 ms (very fast)
- **Sound2Ctl Gain**: Maximum

This creates an on/off effect rather than subtle ducking. The target audio completely cuts out when the trigger sounds, creating stuttering, gated rhythmic patterns.

### Creative Applications:

- Gate a pad with a hi-hat pattern for rhythmic texture
- Gate white noise with a kick pattern for pumping fills
- Gate chord stabs with a rhythmic trigger pattern for syncopation

---

## Tutorial 4: Multi-Band Sidechain (Frequency-Specific Ducking)

![](sidechain_multiband.gif)

Instead of ducking the entire signal, duck only specific frequency ranges.

### Why Use Multi-Band Sidechain:

- Duck only the **low frequencies** of a pad when the bass hits (preserve the high-end shimmer)
- Duck only the **midrange** of guitars when vocals appear (keep bass and treble intact)
- Create more natural, transparent compression

### Setup:

1. After your target instrument, create **multiple Filter modules** to split the signal into frequency bands:
   - **Low band**: Filter (Low Pass) at ~200-300 Hz
   - **Mid band**: Filter (Band Pass) at ~300 Hz - 3 kHz
   - **High band**: Filter (High Pass) at ~3 kHz+
2. Apply sidechain compression (via Compressor + Sound2Ctl) to **only the band(s) you want to duck**
3. Blend the bands back together with an **Amplifier** or route them all to the same output
4. Now only specific frequencies duck while others remain constant

---

## Tutorial 5: Inverse Sidechain (Swelling Effect)

![](sidechain_inverse.gif)

Reverse the typical sidechain behavior - instead of ducking, make the target audio **swell** when the trigger hits.

### Setup:

Instead of using the Sound2Ctl to reduce volume, use it to **increase** volume:

1. Set up the standard sidechain routing (trigger → Sound2Ctl → Compressor)
2. Configure the modulation to **increase** the Compressor's output volume when triggered
3. OR use the Sound2Ctl to modulate an **Amplifier's Volume** parameter upward

### Applications:

- Create swelling pads that emphasize the beat
- Add energy to white noise sweeps synchronized to kicks
- Build tension by having elements grow with each hit

---

## Advanced Tips & Tricks

### 1. Dedicated Trigger Track

Instead of using your actual kick drum to trigger sidechain, create a **separate silent trigger pattern**:
- Create a simple pulse pattern on its own module
- Don't connect it to the Output (it never makes sound)
- Use this silent trigger to control sidechain timing independently of your actual drums
- This lets you adjust sidechain rhythm without changing your actual drum pattern

### 2. Sidechain with LFO (Fake Sidechain)

If you don't have a rhythmic trigger, simulate sidechain pumping with an **LFO module**:
1. Create an LFO set to a rhythmic frequency (e.g., 1/4 notes, 1/8 notes)
2. Route the LFO to modulate a Compressor threshold or Amplifier volume
3. Sync the LFO frequency to your project tempo
4. Adjust the LFO waveform (saw, triangle, or custom) to shape the pump

This creates consistent pumping even without a trigger source, useful for minimalist tracks.

### 3. Parallel Sidechain Compression

For more control, use **parallel compression**:
1. Split your target signal into two paths
2. Apply extreme sidechain compression to one path
3. Leave the other path uncompressed
4. Blend the two signals together
5. This preserves the original dynamics while adding pumping character

### 4. Sample & Hold for Stepped Ducking

Add a **stepped/quantized** quality to sidechain:
1. After the Sound2Ctl, add modulation that quantizes the control signal
2. This creates a "stepped" ducking effect rather than smooth
3. Useful for glitchy, digital aesthetics

---

## Common Mistakes to Avoid

**1. Over-Compression**
- Don't duck more than necessary - start subtle and increase if needed
- More than 6-10 dB of ducking often sounds unnatural (unless you want an extreme effect)

**2. Wrong Release Time**
- Too fast: Pumping sounds jittery and unmusical
- Too slow: Compression doesn't recover in time for the next hit, creating cumulative ducking
- Match the release to your tempo and note timing

**3. Forgetting Makeup Gain**
- Sidechain compression reduces overall level
- Add gain after the Compressor or use the Compressor's output level control to compensate

**4. Triggering with Too Much Audio**
- If your trigger source is too dense (e.g., a full drum loop), the sidechain will constantly compress
- Use isolated triggers (single kick, single snare) for clearer control

---

## Related Techniques

- **Sound2Ctl Module**: [Documentation](../../2--Modules/h--Misc-Modules/Sound2Ctl)
- **Compressor Module**: [Documentation](../../2--Modules/g--Effect-Modules/Compressor)
- **Automation**: [Techniques](../Automation)
- **Parallel Processing**: (See future tutorials)

---

## Example Projects

The following `.sunvox` project files demonstrate each sidechain technique:

1. **`sidechain_basic_edm.sunvox`** - Classic kick-to-bass pumping effect
2. **`sidechain_vocal_clarity.sunvox`** - Subtle vocal ducking for mix clarity
3. **`sidechain_rhythmic_gate.sunvox`** - Extreme gating effect
4. **`sidechain_multiband.sunvox`** - Frequency-specific ducking
5. **`sidechain_inverse.sunvox`** - Swelling effect (reverse sidechain)
6. **`sidechain_lfo_fake.sunvox`** - LFO-based pumping without trigger

Load these projects to see the exact module routing and parameter settings for each technique.

---

_Next Tutorial: [Parallel Processing](../Parallel-Processing)_

[(Sitemap)](../../Sitemap.md)
