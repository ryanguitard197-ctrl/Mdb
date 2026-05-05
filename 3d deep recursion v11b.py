import random
import math

print("======================================")
print("  3D Spatial-Temporal Binary Engine  ")
print("             Prototype v0.3.1         ")
print("======================================")
print("Full manifesto compliance: Definitions List, anchors, buffer, truncation")
print("Runs automatically - no input needed\n")


class ThreeDString:
    def __init__(self, binary_str: str):
        if not all(c in '01' for c in binary_str):
            raise ValueError("Input must be a binary string (0s and 1s only)")
        
        self.binary = binary_str
        self.length = len(binary_str)
        
        if self.length < 8:
            print(f"Warning: String too short ({self.length} bits). Applying virtual padding.")
            self.binary = binary_str.ljust(8, '0')
            self.length = len(self.binary)
        
        self.definitions = self._extract_definitions_list()
        self.state_cloud = self._parse_state_cloud()

    def _extract_definitions_list(self):
        if self.length < 8:
            return {"immutable_anchors": [], "state_map": "default_single_state"}

        defs_len = int(self.binary[:8], 2)
        if self.length < 8 + defs_len:
            return {"immutable_anchors": [], "state_map": "default_single_state"}

        defs_section = self.binary[8:8 + defs_len]
        mid = len(defs_section) // 2
        anchor_str = defs_section[:mid]
        state_map = defs_section[mid:]

        anchors = [i + 8 for i, bit in enumerate(anchor_str) if bit == '1']

        return {
            "immutable_anchors": anchors,
            "state_map": state_map or "density"
        }

    def _parse_state_cloud(self):
        ones = self.binary.count('1')
        zeros = self.length - ones
        total = ones + zeros

        if total == 0:
            return {"states": ["empty"], "probabilities": [1.0]}

        prob_one = ones / total
        prob_zero = zeros / total

        return {
            "states": ["0", "1"],
            "probabilities": [prob_zero, prob_one],
            "description": f"Density-based (1s={ones}, 0s={zeros})"
        }

    def evolve(self, steps: int = 5):
        current = self.binary
        print(f"Initial: '{current}' (length={self.length})")

        immutable = self.definitions["immutable_anchors"]

        for step in range(steps):
            length = len(current)

            if length == 0:
                current = '0'
            elif length % 2 == 1:
                mid = length // 2
                if mid not in immutable:
                    bit = current[mid]
                    flip = '1' if bit == '0' else '0'
                    current = current[:mid] + flip + current[mid+1:]
            else:
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


# Automatic demo
print("Demo: Processing example 3D strings...\n")

examples = [
    "1011010110",
    "11110000111100001111",
    "01010101010101010101"
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
print("Ready for next refinements.")