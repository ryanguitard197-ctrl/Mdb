def demo(start):
    bits = start
    print(f"=== Starting with: '{bits}' (length {len(bits)}) ===\n")
    
    for step in range(1, 16):
        length = len(bits)
        print(f"Step {step:2d} | length = {length} | current: {bits}")
        
        if length % 2 == 1:  # odd length → flip middle bit
            mid = length // 2
            flip = '1' if bits[mid] == '0' else '0'
            new_bits = bits[:mid] + flip + bits[mid+1:]
            print(f"          odd → flip middle → {new_bits}")
        else:                # even length → flip last bit
            flip = '1' if bits[-1] == '0' else '0'
            new_bits = bits[:-1] + flip
            print(f"          even → flip last  → {new_bits}")
        
        bits = new_bits
        print()

# Run a few classic examples
demo('1')
demo('101')
demo('1100')	