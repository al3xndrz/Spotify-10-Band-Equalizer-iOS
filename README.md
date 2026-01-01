# Spotify 10-Band Equalizer for iOS

A tweak that replaces Spotify's default 6-band equalizer with a proper 10-band equalizer.

![10-band EQ](screenshot.jpg)

## Features

- **10 frequency bands**: 31 Hz, 63 Hz, 125 Hz, 250 Hz, 500 Hz, 1 kHz, 2 kHz, 4 kHz, 8 kHz, 16 kHz
- **No jailbreak required** — works with LiveContainer/SideStore
- **Pure Objective-C runtime** — no Substrate dependency

## Requirements

- iPhone with arm64e (A12+)
- iOS 15.0+
- [Theos](https://theos.dev) for building
- LiveContainer or SideStore for installation

## Building

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/Spotify10BandEqualizeriOS.git
cd Spotify10BandEqualizeriOS

# Build
make clean
make
```

The compiled dylib will be at `.theos/obj/arm64e/SpotifyEQ10.dylib`

## Installation (LiveContainer)

1. Build the tweak or download from Releases
2. Copy `SpotifyEQ10.dylib` to:
   ```
   LiveContainer/Documents/Tweaks/spotify/SpotifyEQ10.dylib
   ```
3. Enable tweak injection for Spotify in LiveContainer settings
4. Launch Spotify and open Settings → Playback → Equalizer

## plist Configuration

The equalizer values are stored in `com.spotify.client.plist`:

```
Key: <user_id>.com.spotify.feature.equalizer.values
Value: Array of 10 floats from -1.0 to +1.0
```

Each value corresponds to dB gain: `dB = value × 12` (range: -12 to +12 dB)

### Included Tools

**eq_converter.py** — Convert dB values to plist format:

```bash
# Use a preset
python3 eq_converter.py original.plist output.plist bass_boost

# Custom values (10 dB values from -12 to +12)
python3 eq_converter.py original.plist output.plist 6 4 2 0 -2 -2 0 2 4 6
```

Available presets: `flat`, `bass_boost`, `treble_boost`, `v_shape`, `vocal`, `rock`, `electronic`

## How It Works

The tweak hooks `SPTEqualizerModel` class:
- `values` — expands the gain array from 6 to 10 elements
- `bands` — replaces frequency array with 10 standard frequencies
- `initWithLocalSettings:...` — ensures arrays are expanded on init

Spotify uses Apple's `AUNBandEQ` Audio Unit which supports up to 16 bands, so no audio engine modifications needed.

## Technical Details

| Original (6 bands) | Modified (10 bands) |
|-------------------|---------------------|
| 60 Hz | 31 Hz |
| 150 Hz | 63 Hz |
| 400 Hz | 125 Hz |
| 1 kHz | 250 Hz |
| 2.4 kHz | 500 Hz |
| 15 kHz | 1 kHz |
| — | 2 kHz |
| — | 4 kHz |
| — | 8 kHz |
| — | 16 kHz |

## Troubleshooting

**Tweak not loading:**
- Check Console.app for `[SpotifyEQ10]` logs
- Ensure dylib is in correct path
- Verify tweak injection is enabled in LiveContainer

**Crash on EQ screen:**
- Make sure plist has exactly 10 values (or let tweak expand it)
- Check logs for specific error

## License

MIT License — do whatever you want with it.

## Credits

Built through reverse engineering Spotify.app binary and runtime analysis.
