# 3d_spatial_temporal_v01.py - 3D Spatial-Temporal Binary Engine Prototype v0.1
# =============================================================================
# Implements the manifesto: strings as 3D objects with length-time sync,
# structural protection (Definitions List), and hybrid state-cloud collapse.
# Runs automatically - no input or editing needed.

import random
import math

print("======================================")
print("  3D Spatial-Temporal Binary Engine  ")
print("             Prototype v0.1           ")
print("======================================")
print("Based on Ryan's manifesto (Jan 2025)")
print("Strings treated as 3D objects (value + space + time).")
print("Definitions List protects structure.")
print("State-Cloud Parser + Hybrid Collapse (stochastic + context-guided).\n")


class ThreeDString:
    def __init__(self, binary_str: str):
        if not all(c in '01' for c in binary_str):
            raise ValueError("Input must be a binary string (0s and 1s only)")
        self.binary = binary_str
        self.length = len(binary_str)  # Dimension 2: Space / Dimension 3: Time
        self.definitions = self._extract_definitions()
        self.state_cloud = self._parse_state_cloud()

    def _extract_definitions(self):
        """
        Structural Protection: Protected metadata section.
        For v0.1: First 8 bits = Definitions List length, next N bits = immutable markers + state map.
        """
        if len(self.binary) < 8:
            return {"immutable_markers": [], "state_map": "single_state"}

        header_len = int(self.binary[:8], 2)
        if len(self.binary) < 8 + header_len:
            return {"immutable_markers": [], "state_map": "single_state"}

        defs_section = self.binary[8:8 + header_len]
        # Example: defs_section = immutable bits (first half) + state map code (second half)
        mid = len(defs_section) // 2
        immutable = [i for i, bit in enumerate(defs_section[:mid]) if bit == '1']
        state_map = defs_section[mid:]  # Could be code for parsing rules

        return {
            "immutable_markers": immutable,
            "state_map": state_map or "default"
        }

    def _parse_state_cloud(self):
        """
        State-Cloud Parser: Unpacks the string into multiple potential outcomes.
        For v0.1: Simple density-based cloud (ratio of 1s vs 0s).
        """
        ones = self.binary.count('1')
        zeros = self.length - ones
        total = ones + zeros

        if total == 0:
            return {"states": ["empty"], "probabilities": [1.0]}

        # Basic cloud: two states with density ratios (expandable to more)
        prob_one = ones / total if total > 0 else 0.5
        prob_zero = 1.0 - prob_one

        return {
            "states": ["0", "1"],
            "probabilities": [prob_zero, prob_one],
            "description": f"Density-based (1s={ones}, 0s={zeros})"
        }

    def evolve(self, steps: int = 5):
        """
        Length-Time Synchronization: Length dictates evolution rules.
        Flip middle on odd length, flip end on even length.
        Protects immutable markers.
        """
        current = self.binary
        print(f"Initial: '{current}' (length={self.length})")

        for step in range(steps):
            length = len(current)
            immutable = self.definitions["immutable_markers"]

            if length == 0:
                current = '0'
            elif length % 2 == 1:  # odd → flip middle
                mid = length // 2
                if mid not in immutable:
                    bit = current[mid]
                    flip = '1' if bit == '0' else '0'
                    current = current[:mid] + flip + current[mid+1:]
            else:  # even → flip last
                if length - 1 not in immutable:
                    bit = current[-1]
                    flip = '1' if bit == '0' else '0'
                    current = current[:-1] + flip

            print(f"Step {step+1}: '{current}' (length={length})")

        self.binary = current
        self.length = len(current)
        self.state_cloud = self._parse_state_cloud()  # Re-parse after evolution

    def collapse(self, mode: str = "stochastic"):
        """
        Hybrid Collapse: Stochastic (random) or Context-Guided (calculated).
        """
        cloud = self.state_cloud
        states = cloud["states"]
        probs = cloud["probabilities"]

        if mode == "stochastic":
            # True quantum-like randomness
            chosen = random.choices(states, weights=probs, k=1)[0]
            reason = "stochastic (random)"
        else:
            # Deterministic/context-guided (highest probability)
            chosen = states[probs.index(max(probs))]
            reason = "deterministic (highest probability)"

        print(f"Collapsed to: '{chosen}' ({reason})")
        return chosen


# Demo run - automatic, no input needed
print("Demo: Creating and evolving 3D strings...\n")

examples = [
    "10110101",      # Simple
    "1111000011110000",  # Longer, more density variation
    "0101010101010101"   # Balanced
]

for ex in examples:
    print(f"\nProcessing string: '{ex}'")
    obj = ThreeDString(ex)
    print("Initial state cloud:", obj.state_cloud)
    
    obj.evolve(steps=5)
    print("\nAfter evolution, new state cloud:", obj.state_cloud)
    
    obj.collapse(mode="stochastic")
    obj.collapse(mode="deterministic")
    print("-" * 60)


print("\nPrototype complete. This shows strings as 3D objects with length-time rules,")
print("structural protection, and hybrid collapse - all in regular Python/binary.")
print("Ready for next iteration: recursive definitions, more states, etc.")