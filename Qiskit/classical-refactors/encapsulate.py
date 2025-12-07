import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

class Encapsulate:
    def __init__(self, n_qubits):
        self.n = n_qubits
        self.qc = QuantumCircuit(n_qubits, n_qubits)

    def calculate_optimal_iterations(self, n_qubits, marked=1):
        total_states = 2 ** n_qubits
        return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))


    def _build_oracle(self):
        oracle = QuantumCircuit(self.n)
        oracle.h(self.n-1)
        oracle.mcx(list(range(self.n-1)), self.n-1)
        oracle.h(self.n-1)
        return oracle.to_gate(label="Oracle")
    
    def _build_diffuser(self):
        diffuser = QuantumCircuit(self.n)
        diffuser.h(range(self.n))
        diffuser.x(range(self.n))
        diffuser.h(self.n-1)
        diffuser.mcx(list(range(self.n-1)), self.n-1)
        diffuser.h(self.n-1)
        diffuser.x(range(self.n))
        diffuser.h(range(self.n))
        return diffuser.to_gate(label="Diffuser")
    
    def buildCircuit(self):
        self.qc.h(range(self.n))

        oracle_gate = self._build_oracle()
        diffuser_gate = self._build_diffuser()

        for _ in range(self.calculate_optimal_iterations(self.n)):
            self.qc.append(oracle_gate, range(self.n))
            self.qc.append(diffuser_gate, range(self.n))

        return self.qc

qubits = 5
encapsulator = Encapsulate(qubits)
circuit = encapsulator.buildCircuit()

circuit.measure(range(qubits), range(qubits))

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(circuit, backend)
result = backend.run(compiled, shots=20).result()
counts = result.get_counts()
print(counts)