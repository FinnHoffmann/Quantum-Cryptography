import alice
import bob
import eav
import utils
import simulate

def main():
    n_qubits = 15  # Number of qubits
    eavesdropping_enabled = True  # Toggle eavesdropping on or off

    print("Steps 1-3: Preparing, Eavesdropping (if enabled), and Measuring")
    qubits, alice_bits, alice_bases = alice.prepare_qubits(n_qubits)
    eav_bases = eav.eavsdropping(qubits)
    bob_bases, bob_bits = bob.measure_qubits(qubits)

    if eavesdropping_enabled:
        eav_bases = eav.eavsdropping(qubits)
    else:
        eav_bases = ['-'] * n_qubits  # Placeholder for no eavesdropping

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

    private_key_alice = utils.get_key(alice_bits, matching_bases_alice_bob)
    private_key_bob = utils.get_key(bob_bits, matching_bases_alice_bob)

    print(f"Indices with matching bases (Alice & Bob): {matching_bases_alice_bob}")
    print(f"Indices where Eve's guess is incorrect (potential Bit-Switch): {mismatching_bases_eav}")

    print("\nStep 5: Calculating statistics")
    matching_bases_count = len(matching_bases_alice_bob)
    mismatching_bases_count = len(mismatching_bases_eav)

    # times where Bob guessed right and Eav wrong
    potential_bit_switch_key = len(list(set(matching_bases_alice_bob) & set(mismatching_bases_eav)))

    # (Bob right and Eav wrong) / (Bob right)
    potential_bit_switch_rate = potential_bit_switch_key / len(matching_bases_alice_bob)

    # 
    bit_switches_total = len(utils.mismatching_indices(alice_bits, bob_bits))
    bit_switches_keys = len(utils.mismatching_indices(private_key_alice, private_key_bob))
    actual_bit_switch_rate = (bit_switches_keys / potential_bit_switch_key) if potential_bit_switch_key else 0


    print(f"Proportion of potential Bit-Switch (Eve wrong and Bob correct / Bob correct): {potential_bit_switch_rate:.2f}")
    print(f"Proportion of actual Bit-Switch in Bobs Key (actual / potential): {actual_bit_switch_rate:.2f}")

    print("\nStep 6: Error rate analysis")
    error_rate = utils.calculate_error_rate(private_key_alice, private_key_bob)
    print(f"Alice's private key: {private_key_alice}")
    print(f"Bob's private key:   {private_key_bob}")
    print(f"Overall error rate in private keys (Alice & Bob): {error_rate:.2f}")

    public_key_bob, key_indices = bob.public_key(private_key_bob)
    public_key_alice = [private_key_alice[i] for i in key_indices]

    print(f"Bob publishes this part of his key (and the corresponding indices): {public_key_bob}")
    print(f"Alice publishes her public key: {public_key_alice}")
    error_rate_public = utils.calculate_error_rate(public_key_alice, public_key_bob)
    if error_rate_public > 0.2:
        print("The error rate of the portion of the key that was published is above the threshold -> probably eavsdropping")
    else:
        unpublished_key_alice = [private_key_alice[i] for i in range(len(private_key_alice)) if i not in key_indices]
        unpublished_key_bob = [private_key_bob[i] for i in range(len(private_key_bob)) if i not in key_indices]
        print("The error rate in the published keys is not too high and Alice and Bob continue with the unpublished parts:")
        print(f"Alice unpublished key-part: {unpublished_key_alice}")
        print(f"Bobs unpublished key-part: {unpublished_key_bob}")
        unifyed_key = utils.unify_keys(unpublished_key_alice, unpublished_key_bob)
        print(f"Alice and Bob use Hamming Codes to get the unified Key: {unifyed_key}")

def main_sim():
    potential_bit_switch_rate_mean, actual_bit_switch_rate_mean, error_rate_mean = simulate.average_sim(100, 10)

    print(f"Potential Bit switch rate: {potential_bit_switch_rate_mean}")
    print(f"actual Bit switch rate: {actual_bit_switch_rate_mean}")
    print(f"Error Rate: {error_rate_mean}")


if __name__ == "__main__":
    main()
