from qiskit import QuantumCircuit
import random

def prepare_qubits(n):
    alice_bits = [random.randint(0,1) for _ in range(n)]
    alice_bases = [random.choice(["X","Z"]) for _ in range(n)]

    qubits = QuantumCircuit(n,n)

    for i, (bit, base) in enumerate(zip(alice_bits, alice_bases)):
        if bit == 1:
            qubits.x(i)
        if base == "X":
            qubits.h(i)
    return qubits, alice_bits, alice_bases