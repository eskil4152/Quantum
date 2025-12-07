import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

n = 5
iterations = None

def calculate_optimal_iterations(n_qubits, marked=1):
    total_states = 2 ** n_qubits
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))

iterations = calculate_optimal_iterations(n)

qc = QuantumCircuit(n, n)

qc.h(range(n))

oracle = QuantumCircuit(n)
oracle.h(n-1)
oracle.mcx(list(range(n-1)), n-1)
oracle.h(n-1)
oracle_gate = oracle.to_gate(label="Oracle")

diffuser = QuantumCircuit(n)
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(n-1)
diffuser.mcx(list(range(n-1)), n-1)
diffuser.h(n-1)
diffuser.x(range(n))
diffuser.h(range(n))
diffuser_gate = diffuser.to_gate(label="Diffuser")

for _ in range(iterations):
    #qc.append(oracle_gate, range(n))
    #qc.append(diffuser_gate, range(n))

    # Inlining the oracle gate
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)

    # Inlining the diffuser gate
    qc.h(range(n))
    diffuser.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))

qc.measure(range(n), range(n))

print(qc.draw())

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(qc, backend)
result = backend.run(compiled, shots=100000).result()
counts = result.get_counts()

print("Iterations: ", iterations)
print("Result:", counts)
#plot_histogram(counts).show()