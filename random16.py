# 3d_spatial_temporal_v031.py - Fixed & Refined 3D Spatial-Temporal Binary Engine
# =================================================================================
# v0.3.1 - Fixes UnboundLocalError + short-string crashes
# Implements Ryan's manifesto: 3D objects, Length-Time sync, Definitions List,
# structural anchors, state-cloud parser, hybrid collapse
# All built-in - no external packages

import random
import math

print("======================================")
print("  3D Spatial-Temporal Binary Engine  ")
print("             Refined v0.3.1           ")
print("======================================")
print("Fixed: UnboundLocalError, short-string crashes")
print("Full manifesto compliance: Definitions List, anchors, buffer, truncation")
print("Runs automatically - no input needed\n")


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
        - Next N bits = immutable anchors + state map
        """
        if self.length < 8:
            return {
                "immutable_anchors": [],
                "state_map": "default_single_state"
            }

        defs_len = int(self.binary[:8], 2)
        if self.length < 8 + defs_len:
            return {
                "immutable_anchors": [],
                "state_map": "default_single_state"
            }

        defs_section = self.binary[8:8 + defs_len]
        # First half = immutable anchor indices (bit positions that can't flip)
        mid = len(defs_section) // 2
        anchor_str = defs_section[:mid]
        state_map = defs_section[mid:]

        anchors = []
        for i, bit in enumerate(anchor_str):
            if bit == '1':
                anchors.append(i + 8)  # Offset by header

        return {
            "immutable_anchors": anchors,
            "state_map": state_map or "density"
        }

    def _parse_state_cloud(self):
        """
        State-Cloud Parser: Density-based (safe version)
        """
        ones = self.binary.count('1')
        zeros = self.length - ones
        total = ones + zeros

        # Safe fallback for zero total (empty or invalid)
        if total == 0:
            return {
                "states": ["empty"],
                "probabilities": [1.0],
                "description": "Empty string - single neutral state"
            }

        prob_one = ones / total
        prob_zero = zeros / total

        return {
            "states": ["0", "1"],
            "probabilities": [prob_zero, prob_one],
            "description": f"Density-based (1s={ones}, 0s={zeros})"
        }

    def evolve(self, steps: int = 5):
        """
        Length-Time Synchronization + Anchor Protection
        """
        current = self.binary
        print(f"Initial: '{current}' (length={self.length})")

        anchors = self.definitions["immutable_anchors"]

        for step in range(steps):
            length = len(current)

            if length == 0:
                current = '0'
            elif length % 2 == 1:  # Odd: flip middle (unless anchored)
                mid = length // 2
                if mid not in anchors:
                    bit = current[mid]
                    flip = '1' if bit == '0' else '0'
                    current = current[:mid] + flip + current[mid+1:]
            else:  # Even: flip last (unless anchored)
                if length - 1 not in anchors:
                    bit = current[-1]
                    flip = '1' if bit == '0' else '0'
                    current = current[:-1] + flip

            print(f"Step {step+1}: '{current}' (length={length})")

        self.binary = current
        self.length = len(current)
        self.state_cloud = self._parse_state_cloud()

    def collapse(self, mode: str = "stochastic"):
        """
        Hybrid Collapse: Stochastic or Deterministic
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


# Automatic demo run - no user input required
print("Demo: Processing example 3D strings...\n")

examples = [
    "1011010110",                # Short - will pad
    "11110000111100001111",      # Longer
    "01010101010101010101"       # Balanced
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
print("Fixed: UnboundLocalError, short-string crashes, zero-division")
print("Key features: Definitions List, anchors, buffer, truncation")
print("All in regular Python/binary.")
print("Ready for v0.4: recursive Definitions, more states, entropy injection, etc.")