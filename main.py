import alice
import bob
import eav
import utils

def main():
    n = 10  # Number of qubits
    eavesdropping_enabled = True  # Toggle eavesdropping on or off

    print("Steps 1-3: Preparing, Eavesdropping (if enabled), and Measuring")
    qubits, alice_bits, alice_bases = alice.prepare_qubits(n)

    if eavesdropping_enabled:
        eav_bases = eav.eavsdropping(qubits)
    else:
        eav_bases = ['-'] * n  # Placeholder for no eavesdropping

    bob_bases, bob_bits = bob.measure_qubits(qubits)

    # Formatted output for comparison
    print("\nBases and Bits Comparison:")
    print(f"{'Alice Bases':<15}{'Eve Bases':<15}{'Bob Bases':<15}")
    print(f"{'=' * 45}")
    for a, e, b in zip(alice_bases, eav_bases, bob_bases):
        print(f"{a:<15}{e:<15}{b:<15}")

    print("\nBits Comparison:")
    print(f"{'Alice Bits':<15}{'':<15}{'Bob Bits':<15}")
    print(f"{'=' * 45}")
    for a_bit, b_bit in zip(alice_bits, bob_bits):
        print(f"{a_bit:<15}{'':<15}{b_bit:<15}")

    print("\nStep 4: Analyzing matching and mismatching bases")
    matching_bases_alice_bob = utils.matching_indices(alice_bases, bob_bases)
    mismatching_bases_eav = utils.mismatching_indices(alice_bases, eav_bases)

    shared_key_alice = utils.get_key(alice_bits, matching_bases_alice_bob)
    shared_key_bob = utils.get_key(bob_bits, matching_bases_alice_bob)

    print(f"Indices with matching bases (Alice & Bob): {matching_bases_alice_bob}")
    print(f"Indices where Eve's guess is incorrect (potential Bit-Switch): {mismatching_bases_eav}")

    print("\nStep 5: Calculating statistics")
    matching_bases_count = len(matching_bases_alice_bob)
    mismatching_bases_count = len(mismatching_bases_eav)

    potential_bit_switch_key = len(list(set(matching_bases_alice_bob) & set(mismatching_bases_eav)))
    potential_bit_switch_rate = potential_bit_switch_key / len(matching_bases_alice_bob)
    bit_switchs_total = len(utils.mismatching_indices(alice_bits, bob_bits))
    bit_switchs_keys = len(utils.mismatching_indices(shared_key_alice, shared_key_bob))
    actual_bit_switch_rate = (bit_switchs_keys / potential_bit_switch_key) if potential_bit_switch_key else 0


    print(f"Proportion of potential Bit-Switch (Eve wrong and Bob correct / Bob correct): {potential_bit_switch_rate:.2f}")
    print(f"Proportion of actual Bit-Switch in Bobs Key (actual / potential): {actual_bit_switch_rate:.2f}")

    print("\nStep 6: Error rate analysis")
    error_rate = utils.calculate_error_rate(shared_key_alice, shared_key_bob)
    print(f"Alice's shared key: {shared_key_alice}")
    print(f"Bob's shared key:   {shared_key_bob}")
    print(f"Overall error rate in shared keys (Alice & Bob): {error_rate:.2f}")

if __name__ == "__main__":
    main()
