from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

n = 2

qc = QuantumCircuit(n, n)

qc.h(range(n))

oracle = QuantumCircuit(n)
oracle.cz(0, 1)
oracle_gate = oracle.to_gate(label="Oracle")

diffuser = QuantumCircuit(n)
diffuser.h(range(n))
diffuser.x(range(n))
diffuser.h(1)
diffuser.cx(0, 1)
diffuser.h(1)
diffuser.x(range(n))
diffuser.h(range(n))
diffuser_gate = diffuser.to_gate(label="Diffuser")

qc.append(oracle_gate, range(n))
qc.append(diffuser_gate, range(n))

qc.measure(range(n), range(n))

print(qc.draw())

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(qc, backend)
result = backend.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Result:", counts)
plot_histogram(counts).show()