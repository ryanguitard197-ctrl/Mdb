# 3d_superbit_v01.py - 3D Binary Super-Bit Engine v0.1
# ====================================================
# Each string is a self-describing multi-state super-bit

class SuperBit:
    def __init__(self, binary_str):
        if not all(c in '01' for c in binary_str):
            raise ValueError("Input must be a binary string (0s and 1s only)")
        self.full_string = binary_str
        self.state_cloud = self._parse_declaration()
        self.current_collapse = None  # None = full multi-state; str = collapsed value

    def _parse_declaration(self):
        """Parse recursive/nested state declaration from start of string"""
        s = self.full_string
        
        if len(s) < 4:
            return {"num_states": 1, "states": [s], "weights": [1.0]}  # fallback single state
        
        # First 4 bits = length of declaration (0-15 bits for simplicity)
        header_len = int(s[:4], 2)
        if len(s) < 4 + header_len:
            return {"num_states": 1, "states": [s], "weights": [1.0]}
        
        declaration = s[4:4+header_len]
        payload = s[4+header_len:]
        
        # For v0.1: declaration = num_states (first 4 bits) + crude weights (rest)
        num_states = int(declaration[:4], 2) or 1  # 0 means 1
        weight_bits = declaration[4:]
        
        # Distribute crude weights (each bit 0=0.0, 1=1.0; normalize later)
        weights = [int(b) for b in weight_bits.ljust(num_states, '0')[:num_states]]
        total = sum(weights)
        if total == 0:
            weights = [1.0 / num_states] * num_states
        else:
            weights = [w / total for w in weights]
        
        # States = split payload or default to indices
        states = [payload[i::num_states] for i in range(num_states)] if payload else [str(i) for i in range(num_states)]
        
        return {
            "num_states": num_states,
            "states": states,
            "weights": weights
        }

    def collapse(self, context_preference=None):
        """Collapse to one definite state, guided by optional context (e.g. prefer '1')"""
        if self.current_collapse is not None:
            return self.current_collapse
        
        cloud = self.state_cloud
        weights = cloud["weights"]
        states = cloud["states"]
        
        # Simple context-guided collapse for v0.1
        if context_preference == 'prefer_1':
            # Boost weight for states containing '1'
            boosted = [w * (2 if '1' in st else 1) for w, st in zip(weights, states)]
            total = sum(boosted)
            probs = [b / total for b in boosted]
        else:
            probs = weights
        
        # Pick highest probability (deterministic for now)
        chosen_idx = probs.index(max(probs))
        self.current_collapse = states[chosen_idx]
        
        return self.current_collapse

    def re_expand(self):
        """Return to full multi-state (clear collapse)"""
        self.current_collapse = None

    def __str__(self):
        cloud = self.state_cloud
        return (f"SuperBit(num_states={cloud['num_states']}, "
                f"weights={cloud['weights'][:5]}{'...' if len(cloud['weights']) > 5 else ''}, "
                f"collapsed={self.current_collapse})")

    def __repr__(self):
        return self.__str__()


# Smoke test / demo
if __name__ == "__main__":
    print("=== 3D Super-Bit Engine v0.1 Smoke Test ===\n")
    
    # Example: 3-state super-bit (header 0011 = len 3, then 0011 for num_states=3)
    sb = SuperBit("001100111010101")  # header len=3, declaration=001 (num_states=3), payload=11010101
    print("Created:", sb)
    
    print("\nFull state cloud:")
    print("  States:", sb.state_cloud["states"])
    print("  Weights:", sb.state_cloud["weights"])
    
    print("\nCollapse (default):", sb.collapse())
    print("Collapse (prefer 1):", sb.collapse(context_preference='prefer_1'))
    
    sb.re_expand()
    print("After re-expand:", sb)