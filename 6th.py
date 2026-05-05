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