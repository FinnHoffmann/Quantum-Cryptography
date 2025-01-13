from alice import prepare_qubits, send_qubits
from bob import measure_qubits
from utils import compare_keys

def main():
    # Number of qubits to be used
    n = 5

    # Alice: Prepare qubits and choose random bases
    alice_bits, alice_bases, qubits = prepare_qubits(n)
    print(f"Alice's bits: {alice_bits}")
    print(f"Alice's bases: {alice_bases}")

    # Bob: Choose random bases and measure the received qubits
    bob_bases, bob_bits = measure_qubits(qubits)
    print(f"Bob's bases: {bob_bases}")
    print(f"Bob's measured bits: {bob_bits}")

    # Compare keys and derive the final shared key
    alice_key, bob_key = compare_keys(alice_bits, alice_bases, bob_bases, bob_bits)
    print(f"Alice's final key: {alice_key}")
    print(f"Bob's final key: {bob_key}")

    # Output the result
    print(f"Final agreed key: {alice_key}")

if __name__ == "__main__":
    main()
