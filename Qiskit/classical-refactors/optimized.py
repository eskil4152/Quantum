from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer

from helper import *

number_of_qubits = 5

main_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)
main_circuit.h(range(number_of_qubits))

for _ in range(calculate_optimal_iterations(number_of_qubits)):
    main_circuit.append(get_oracle_gate(number_of_qubits), range(number_of_qubits))
    main_circuit.append(get_diffuser_gate(number_of_qubits), range(number_of_qubits))

main_circuit.measure(range(number_of_qubits), range(number_of_qubits))

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(main_circuit, backend)
result = backend.run(compiled, shots=100000).result()
counts = result.get_counts()

print("Result:", counts)


def calculate_optimal_iterations(n_qubits, marked=1):
    total_states = 2 ** n_qubits
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))