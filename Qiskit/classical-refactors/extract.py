import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

n = 5
iterations = None

def calculate_optimal_iterations(n_qubits, marked=1):
    total_states = 2 ** n_qubits
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))

def oracle_gate(n_qubits):
    oracle = QuantumCircuit(n_qubits)
    oracle.h(n_qubits-1)
    oracle.mcx(list(range(n_qubits-1)), n_qubits-1)
    oracle.h(n_qubits-1)
    oracle_gate = oracle.to_gate(label="Oracle")
    return oracle_gate

def diffuser_gate(n_qubits):
    diffuser = QuantumCircuit(n_qubits)
    diffuser.h(range(n_qubits))
    diffuser.x(range(n_qubits))
    diffuser.h(n_qubits-1)
    diffuser.mcx(list(range(n_qubits-1)), n_qubits-1)
    diffuser.h(n_qubits-1)
    diffuser.x(range(n_qubits))
    diffuser.h(range(n_qubits))
    diffuser_gate = diffuser.to_gate(label="Diffuser")
    return diffuser_gate

iterations = calculate_optimal_iterations(n)

qc = QuantumCircuit(n, n)

qc.h(range(n))

for _ in range(iterations):
    qc.append(oracle_gate(n), range(n))
    qc.append(diffuser_gate(n), range(n))

qc.measure(range(n), range(n))

print(qc.draw())

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(qc, backend)
result = backend.run(compiled, shots=100000).result()
counts = result.get_counts()

print("Iterations: ", iterations)
print("Result:", counts)
#plot_histogram(counts).show()