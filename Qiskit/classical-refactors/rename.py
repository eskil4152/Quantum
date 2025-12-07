import math
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram

number_of_qubits = 2
iterations = None

def calculate_optimal_iterations(n_qubits, marked=1):
    total_states = 2 ** n_qubits
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(total_states / marked))))

iterations = calculate_optimal_iterations(number_of_qubits)

main_circuit = QuantumCircuit(number_of_qubits, number_of_qubits)

main_circuit.h(range(number_of_qubits))

oracle_circuit = QuantumCircuit(number_of_qubits)
oracle_circuit.cz(0, 1)
oracle_gate = oracle_circuit.to_gate(label="Oracle")

diffuser_circuit = QuantumCircuit(number_of_qubits)
diffuser_circuit.h(range(number_of_qubits))
diffuser_circuit.x(range(number_of_qubits))
diffuser_circuit.h(1)
diffuser_circuit.cx(0, 1)
diffuser_circuit.h(1)
diffuser_circuit.x(range(number_of_qubits))
diffuser_circuit.h(range(number_of_qubits))
diffuser_gate = diffuser_circuit.to_gate(label="Diffuser")

for _ in range(iterations):
    main_circuit.append(oracle_gate, range(number_of_qubits))
    main_circuit.append(diffuser_gate, range(number_of_qubits))

main_circuit.measure(range(number_of_qubits), range(number_of_qubits))

print(main_circuit.draw())

backend = Aer.get_backend("qasm_simulator")
compiled = transpile(main_circuit, backend)
result = backend.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Result:", counts)
plot_histogram(counts).show()