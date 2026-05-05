# 3dbase_v01.py - 3D Binary Core Engine v0.1
# ==========================================
# Core: binary strings evolve using length as simulated time dimension

class ThreeDBinary:
    def __init__(self, seed="101"):
        """Initialize with a binary string seed (str of '0's and '1's)"""
        if not isinstance(seed, str) or not all(c in '01' for c in seed):
            raise ValueError("Seed must be a string containing only '0' and '1'")
        self.current = seed
        self.history = [seed]

    def step(self):
        """Perform one evolution step using length-as-time rule"""
        length = len(self.current)
        
        if length == 0:
            self.current = '0'
        elif length % 2 == 1:  # odd length → flip middle bit
            mid = length // 2
            bit = self.current[mid]
            flip = '1' if bit == '0' else '0'
            self.current = self.current[:mid] + flip + self.current[mid+1:]
        else:  # even length → flip last bit
            bit = self.current[-1]
            flip = '1' if bit == '0' else '0'
            self.current = self.current[:-1] + flip
            
        self.history.append(self.current)
        return self.current

    def evolve(self, steps=10):
        """Evolve for N steps, return final state"""
        for _ in range(steps):
            self.step()
        return self.current

    def get_history(self):
        """Return list of all states seen so far"""
        return self.history.copy()

    def unpack_to_floats(self, count=4):
        """Simple utility: unpack recent states to normalized floats (0.0-1.0)"""
        if len(self.history) < count:
            self.evolve(steps=count - len(self.history))
        recent = self.history[-count:]
        return [int(state, 2) / (2**len(state) - 1) if state else 0.0 for state in recent]

    def __str__(self):
        return f"3DBinary(current='{self.current}', len={len(self.current)}, steps={len(self.history)-1})"

    def __repr__(self):
        return self.__str__()


# Smoke test / demo when run directly
if __name__ == "__main__":
    print("3D Binary Engine v0.1 - Smoke Test\n" + "="*40 + "\n")
    
    engine = ThreeDBinary("101")
    print("Initial state:", engine)
    
    print("\nEvolving 10 steps...")
    final = engine.evolve(steps=10)
    print("Final state:", engine)
    
    print("\nFull history:")
    for i, state in enumerate(engine.get_history()):
        print(f"  Step {i:2d}: '{state}' (len={len(state)})")
    
    print("\nUnpack last 4 states to floats:")
    floats = engine.unpack_to_floats(count=4)
    print("Floats:", floats)