import random
from qiskit import QuantumCircuit, Aer, transpile, assemble

def prepare_qubits(n):
    """
    Prepares qubits with random bit values and bases.
    Returns the bits, bases, and a list of QuantumCircuits.
    """
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['Z', 'X']) for _ in range(n)]

    qubits = []
    for bit, basis in zip(alice_bits, alice_bases):
        qc = QuantumCircuit(1, 1)
        if bit == 1:
            qc.x(0)  # Apply X-gate for bit value 1
        if basis == 'X':
            qc.h(0)  # Apply H-gate for X-basis
        qubits.append(qc)

    return alice_bits, alice_bases, qubits