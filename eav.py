import random
from qiskit import transpile
from qiskit_aer import Aer

def eavsdropping(qubits):
    simulator = Aer.get_backend('qasm_simulator')
    n = qubits.num_qubits

    eav_bases = [random.choice(["X","Z"]) for _ in range(n)]

    for i in range(n):
        if eav_bases[i] == "X":
            qubits.h(i)
    qubits.measure(range(n),range(n))

    return eav_bases
