def bin_to_float(b):
    if not b: return 0.0
    return int(b, 2) / (2 ** len(b) - 1 if len(b) > 0 else 1)

short_seed = '101'          # Change this tiny seed to whatever you want

amplitudes = []
current = short_seed

for i in range(4):          # Generate 4 amplitudes for 2-qubit state
    # Use length as time to decide next action
    new_bit = '1' if len(current) % 2 == 0 else '0'
    current += new_bit
    
    # Simple mix: rotate left + invert where bits match previous
    rotated = current[1:] + current[0]
    current = ''.join('1' if c != r else '0' for c, r in zip(current, rotated))
    
    amp = bin_to_float(current)
    amplitudes.append(amp)

print("Generated amplitudes from 3-bit seed:", amplitudes)

# Normalize manually (sqrt of sum of squares)
total_sq = sum(a * a for a in amplitudes)
norm = total_sq ** 0.5 if total_sq > 0 else 1
state = [a / norm for a in amplitudes]

print("\nInitial state vector (normalized):", state)

# Toy Hadamard on first qubit (manual matrix multiply for 2 qubits)
h = [0.7071, 0.7071]   # approx 1/sqrt(2)
result = [0, 0, 0, 0]

result[0] = h[0] * state[0] + h[1] * state[2]
result[1] = h[0] * state[1] + h[1] * state[3]
result[2] = h[1] * state[0] - h[0] * state[2]
result[3] = h[1] * state[1] - h[0] * state[3]

print("After Hadamard on first qubit:", [round(x, 4) for x in result])

# Simple measurement probabilities
probs = [round(abs(x)**2, 4) for x in result]
print("Measurement probabilities (00, 01, 10, 11):", probs)
import numpy as np  # Basic math (runs on anything)

def bin_to_float(b):
    if not b: return 0.0
    return int(b, 2) / (2**len(b) - 1)

short_seed = '101'  # Tiny 3-bit seed - this is all we 'store/transmit'

# Evolve using length as time dimension to mix/generate 4 amplitudes
amplitudes = []
current = short_seed
for i in range(4):  # 4 states for 2 qubits
    new_bit = '1' if len(current) % 2 == 0 else '0'  # Length decides append
    current += new_bit
    shifted = current[1:] + current[0]  # Shift for mix
    current = ''.join('1' if c != s else '0' for c, s in zip(current, shifted))  # XOR-like with shift
    amp = bin_to_float(current)
    amplitudes.append(amp)

print(f"Generated amplitudes from 3 bits: {amplitudes}")

# Normalize to valid quantum state (real amps for simplicity)
norm = np.sqrt(sum(a**2 for a in amplitudes))
state_vec = np.array([a / norm for a in amplitudes])

# Toy quantum sim: 2-qubit state
# (Normally needs libraries like QuTiP, but here's manual Hadamard apply for Pentium-level)
H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)  # Hadamard matrix
I = np.eye(2)  # Identity
H1 = np.kron(H, I)  # Tensor for first qubit
psi = state_vec.reshape(4, 1)  # Column vector
result = H1 @ psi
probs = [abs(c[0])**2 for c in result]

print(f"Initial state vec: {psi.flatten()}")
print(f"After Hadamard on first qubit: {result.flatten()}")
print(f"Measurement probs (00,01,10,11): {probs}")