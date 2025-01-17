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

# def public_key(bob_key, percentage = 20):
#     # percantage of the key to be published
#     count_float = len(bob_key) * (percentage / 100)
#     count = int(count_float) + (count_float > int(count_float))
#     selected_indices = []
#     selected_elements = []
#     for _ in range(count):
#         index = random.randint(0, len(bob_key) - 1)
#         selected_indices.append(index)
#         selected_elements.append(bob_key.pop(index))
#     return selected_elements, selected_indices

def public_key(bob_key, percentage=20):
    # Percentage of the key to be published
    count_float = len(bob_key) * (percentage / 100)
    count = int(count_float) + (count_float > int(count_float))
    selected_indices = []
    selected_elements = []
    
    # Randomly select the indices without removing elements
    while len(selected_elements) < count:
        index = random.randint(0, len(bob_key) - 1)
        if index not in selected_indices:  # Ensure no duplicates
            selected_indices.append(index)
            selected_elements.append(bob_key[index])  # No pop, just access
    return selected_elements, selected_indices