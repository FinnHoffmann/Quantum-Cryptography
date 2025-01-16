import random
from qiskit import transpile
from qiskit_aer import Aer

def measure_qubits(qubits):
    simulator = Aer.get_backend('qasm_simulator')
    n = qubits.num_qubits

    bob_bases = [random.choice(["X","Z"]) for _ in range(n)]

    for i in range(n):
        if bob_bases[i] == "X":
            qubits.h(i)
    qubits.measure(range(n),range(n))
    
    transpiled_qubits = transpile(qubits, simulator)
    job = simulator.run(transpiled_qubits, shots=1)

    bob_bits_string = list(((job.result()).get_counts()).keys())[0]
    bob_bits = [int(bit) for bit in bob_bits_string][::-1]

    return bob_bases, bob_bits
