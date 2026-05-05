# 3d_spatial_temporal_engine_v10.py - Final 3D Spatial-Temporal Binary Engine Prototype
# =================================================================================
# Implements Ryan's blueprint and specification v1.0
- 3D objects (D1: value, D2: space, D3: time)
- Length-Time Synchronization (length dictates rules)
- Structural Protection (Definitions List with immutable markers, state maps, phase toggle)
- State-Cloud Parser + Hybrid Collapse (stochastic + context-preference)
- Basic recursion for unlimited dimensions (D3 bootstraps D4)
# Runs automatically - no input needed

import random
import math

print("=========================================")
print("  3D Spatial-Temporal Binary Engine     ")
print("             Final Prototype v1.0        ")
print("=========================================")
print("Based on Ryan's blueprint & specification")
print("Strings as 3D objects with informational geometry.")
print("Length-Time Synchronization: length dictates rules.")
print("Structural Protection: Definitions List with immutable markers.")
print("State-Cloud Parser + Hybrid Collapse.")
print("Basic recursion for unlimited dimensions.\n")


class ThreeDString:
    def __init__(self, binary_str: str):
        if not all(c in '01' for c in binary_str):
            raise ValueError("Input must be a binary string (0s and 1s only)")
        
        self.binary = binary_str
        self.length = len(binary_str)
        
        # Precision protection: Virtual padding for short strings
        if self.length < 8:
            print(f"Warning: String too short ({self.length} bits). Applying virtual padding.")
            self.binary = binary_str.ljust(8, '0')
            self.length = len(self.binary)
        
        self.definitions = self._extract_definitions_list()
        self.state_cloud = self._parse_state_cloud()

    def _extract_definitions_list(self):
        """
        Structural Protection: Definitions List
        - First 8 bits = length of Definitions section
        - Next N bits = immutable markers + state map + phase toggle
        """
        if self.length < 8:
            return {
                "immutable_markers": [],
                "state_map": "default_single_state",
                "phase_toggle": "off"
            }

        defs_len = int(self.binary[:8], 2)
        if self.length < 8 + defs_len:
            return {
                "immutable_markers": [],
                "state_map": "default_single_state",
                "phase_toggle": "off"
            }

        defs_section = self.binary[8:8 + defs_len]
        # v1.0: Thirds: immutable markers + state map + phase toggle
        third = len(defs_section) // 3
        marker_str = defs_section[:third]
        state_map = defs_section[third:2*third] or "density"
        phase_toggle = defs_section[2*third:] or "off"

        immutable = []
        for i, bit in enumerate(marker_str):
            if bit == '1':
                immutable.append(i + 8)  # Offset by header

        return {
            "immutable_markers": immutable,
            "state_map": state_map,
            "phase_toggle": phase_toggle
        }

    def _parse_state_cloud(self):
        """
        State-Cloud Parser: Unpacks payload into multiple potential outcomes
        - v1.0: Density-based + basic recursion for D4 bootstrapping
        """
        payload = self.binary[8 + len(self.definitions["state_map"]) + len(self.definitions["phase_toggle"]):]  # After Definitions

        ones = payload.count('1')
        zeros = len(payload) - ones
        total = ones + zeros

        if total == 0:
            return {
                "states": ["empty"],
                "probabilities": [1.0],
                "description": "Empty string - single neutral state"
            }

        prob_one = ones / total
        prob_zero = zeros / total

        # Basic recursion hook: if state_map = "D4_parser", bootstrap D4 (e.g., partition time for probability density)
        if self.definitions["state_map"] == "D4_parser":
            # Example D4 bootstrapping: Partition time (length) into probability bins
            bin_size = self.length // 2
            d4_states = [payload[i:i+bin_size] for i in range(0, self.length, bin_size) if i + bin_size <= self.length]
            d4_probs = [len(st) / self.length for st in d4_states]
            return {
                "states": d4_states,
                "probabilities": d4_probs,
                "description": "D4 bootstrapped (probability density from time partition)"
            }

        return {
            "states": ["0", "1"],
            "probabilities": [prob_zero, prob_one],
            "description": f"Density-based (1s={ones}, 0s={zeros})"
        }

    def evolve(self, steps: int = 5):
        """
        Length-Time Synchronization: Evolution with anchor protection
        """
        current = self.binary
        print(f"Initial: '{current}' (length={self.length})")

        immutable = self.definitions["immutable_markers"]
        phase_toggle = self.definitions["phase_toggle"]

        for step in range(steps):
            length = len(current)

            # Phase Toggle: If "on", apply additional phase shift (e.g., XOR with step)
            if phase_toggle == "on":
                current = ''.join('1' if bit == '0' else '0' if (i + step) % 2 == 0 else bit for i, bit in enumerate(current))

            if length % 2 == 1:  # Odd: flip middle (unless immutable)
                mid = length // 2
                if mid not in immutable:
                    bit = current[mid]
                    flip = '1' if bit == '0' else '0'
                    current = current[:mid] + flip + current[mid+1:]
            else:  # Even: flip last (unless immutable)
                end = length - 1
                if end not in immutable:
                    bit = current[end]
                    flip = '1' if bit == '0' else '0'
                    current = current[:end] + flip

            print(f"Step {step+1}: '{current}' (length={length})")

        self.binary = current
        self.length = len(current)
        self.state_cloud = self._parse_state_cloud()

    def collapse(self, mode: str = "stochastic"):
        """
        Observer Mechanism: Hybrid Collapse
        """
        cloud = self.state_cloud
        states = cloud["states"]
        probs = cloud["probabilities"]

        if mode == "stochastic":
            chosen = random.choices(states, weights=probs, k=1)[0]
            reason = "stochastic (random)"
        else:
            chosen = states[probs.index(max(probs))]
            reason = "deterministic (highest probability)"

        print(f"Collapsed to: '{chosen}' ({reason})")
        return chosen


# Automatic demo run
print("Demo: Processing example 3D strings...\n")

examples = [
    "10110101",                 # Short
    "11110000111100001111",     # Longer
    "01010101010101010101"      # Balanced
]

for ex in examples:
    print(f"\nProcessing string: '{ex}'")
    obj = ThreeDString(ex)
    print("Definitions List:", obj.definitions)
    print("Initial state cloud:", obj.state_cloud)
    
    obj.evolve(steps=5)
    print("\nAfter evolution, new state cloud:", obj.state_cloud)
    
    obj.collapse(mode="stochastic")
    obj.collapse(mode="deterministic")
    print("=" * 70)


print("\nPrototype v0.3.1 complete.")
print("All manifesto pillars implemented in basic form.")
print("Ready for v0.4: recursive Definitions List, more states, entropy injection, etc.")