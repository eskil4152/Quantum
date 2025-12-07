import math
from qiskit import QuantumCircuit

def calculate_optimal_iterations(n_qubits, marked=1):
    total_states = 2 ** n_qubits
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))

def get_oracle_gate(n_qubits):
    oracle = QuantumCircuit(n_qubits)
    oracle.h(n_qubits-1)
    oracle.mcx(list(range(n_qubits-1)), n_qubits-1)
    oracle.h(n_qubits-1)
    return oracle.to_gate(label="Oracle")

def get_diffuser_gate(n_qubits):
    diffuser = QuantumCircuit(n_qubits)
    diffuser.h(range(n_qubits))
    diffuser.x(range(n_qubits))
    diffuser.h(n_qubits-1)
    diffuser.mcx(list(range(n_qubits-1)), n_qubits-1)
    diffuser.h(n_qubits-1)
    diffuser.x(range(n_qubits))
    diffuser.h(range(n_qubits))
    return diffuser.to_gate(label="Diffuser")