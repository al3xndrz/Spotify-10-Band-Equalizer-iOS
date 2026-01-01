#!/usr/bin/env python3
"""
SpotifyEQ10 - dB to plist converter
Converts dB values (-12 to +12) to Spotify plist format (-1.0 to +1.0)

Standard 10-band frequencies:
  Band 1:  31 Hz
  Band 2:  63 Hz
  Band 3:  125 Hz
  Band 4:  250 Hz
  Band 5:  500 Hz
  Band 6:  1 kHz
  Band 7:  2 kHz
  Band 8:  4 kHz
  Band 9:  8 kHz
  Band 10: 16 kHz
"""

import plistlib
import sys

def db_to_value(db):
    """Convert dB (-12 to +12) to plist value (-1.0 to +1.0)"""
    return max(-1.0, min(1.0, db / 12.0))

def value_to_db(value):
    """Convert plist value (-1.0 to +1.0) to dB (-12 to +12)"""
    return value * 12.0

# Example presets (dB values)
PRESETS = {
    "flat": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    "bass_boost": [6, 5, 4, 2, 0, 0, 0, 0, 0, 0],
    "treble_boost": [0, 0, 0, 0, 0, 0, 2, 4, 5, 6],
    "v_shape": [5, 4, 2, 0, -2, -2, 0, 2, 4, 5],
    "vocal": [-2, -1, 0, 2, 4, 4, 2, 0, -1, -2],
    "rock": [4, 3, 2, 0, -1, -1, 0, 2, 3, 4],
    "electronic": [4, 3, 0, -2, -1, 0, 2, 3, 4, 3],
}

def create_plist(input_plist_path, output_plist_path, db_values):
    """Create modified plist with custom EQ values"""
    
    # Read original plist
    with open(input_plist_path, 'rb') as f:
        data = plistlib.load(f)
    
    # Find equalizer values key
    eq_key = None
    for k in data.keys():
        if 'equalizer.values' in k:
            eq_key = k
            break
    
    if not eq_key:
        print("Error: equalizer.values key not found in plist")
        return False
    
    # Convert dB to plist values
    plist_values = [db_to_value(db) for db in db_values]
    
    # Update plist
    data[eq_key] = plist_values
    
    # Save
    with open(output_plist_path, 'wb') as f:
        plistlib.dump(data, f)
    
    print(f"Created: {output_plist_path}")
    print(f"dB values: {db_values}")
    print(f"Plist values: {[round(v, 3) for v in plist_values]}")
    return True

def print_usage():
    print("Usage:")
    print("  python eq_converter.py <input.plist> <output.plist> <preset_name>")
    print("  python eq_converter.py <input.plist> <output.plist> <db1> <db2> ... <db10>")
    print("")
    print("Available presets:", ", ".join(PRESETS.keys()))
    print("")
    print("Example:")
    print("  python eq_converter.py original.plist custom.plist bass_boost")
    print("  python eq_converter.py original.plist custom.plist 6 4 2 0 -2 -2 0 2 4 6")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print_usage()
        sys.exit(1)
    
    input_plist = sys.argv[1]
    output_plist = sys.argv[2]
    
    if len(sys.argv) == 4:
        # Preset name
        preset_name = sys.argv[3].lower()
        if preset_name not in PRESETS:
            print(f"Unknown preset: {preset_name}")
            print("Available presets:", ", ".join(PRESETS.keys()))
            sys.exit(1)
        db_values = PRESETS[preset_name]
    else:
        # Custom dB values
        try:
            db_values = [float(x) for x in sys.argv[3:13]]
            if len(db_values) < 10:
                db_values.extend([0] * (10 - len(db_values)))
        except ValueError:
            print("Error: dB values must be numbers")
            sys.exit(1)
    
    create_plist(input_plist, output_plist, db_values)
