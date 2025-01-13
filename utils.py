def compare_keys(alice_bits, alice_bases, bob_bases, bob_bits):
    """
    Matches the bases between Alice and Bob and derives the shared key.
    """
    shared_key_alice = []
    shared_key_bob = []

    for a_bit, a_basis, b_basis, b_bit in zip(alice_bits, alice_bases, bob_bases, bob_bits):
        if a_basis == b_basis:
            shared_key_alice.append(a_bit)
            shared_key_bob.append(b_bit)

    if shared_key_alice != shared_key_bob:
        print("Warning: Keys do not fully match! Possible eavesdropping detected.")

    return shared_key_alice, shared_key_bob

def error_rate(alice_key, bob_key):
    errors = sum(a != b for a, b in zip(alice_key, bob_key))
    error_rate = errors / len(alice_key)
    return error_rate