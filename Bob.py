import random
from qiskit import transpile
from qiskit_aer import Aer

def measure_qubits(qubits):
    """
    Measures received qubits with random bases.
    Returns the bases chosen by Bob and the measurement results.
    """
    simulator = Aer.get_backend('qasm_simulator')

    bob_bases = [random.choice(['Z', 'X']) for _ in qubits]
    bob_bits = []

    for qc, basis in zip(qubits, bob_bases):
        qc_copy = qc.copy()
        if basis == 'X':
            qc_copy.h(0)  # Apply H-gate to switch to X-basis
        qc_copy.measure_all()

        # Transpile and run the circuit
        transpiled_circuit = transpile(qc_copy, simulator)
        result = simulator.run(transpiled_circuit, shots=1).result()
        measured_bit = int(list(result.get_counts().keys())[0])  # Get the measured bit
        bob_bits.append(measured_bit)

    return bob_bases, bob_bits