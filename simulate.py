import alice
import bob
import eav
import utils

def simulate_BB84(n_qubits):
    qubits, alice_bits, alice_bases = alice.prepare_qubits(n_qubits)
    eav_bases = eav.eavsdropping(qubits)
    bob_bases, bob_bits = bob.measure_qubits(qubits)

    return alice_bases, alice_bits, bob_bases, bob_bits, eav_bases

def get_statistic(alice_bases, alice_bits, bob_bases, bob_bits, eav_bases):
    matching_bases_alice_bob = utils.matching_indices(alice_bases, bob_bases)
    mismatching_bases_eav = utils.mismatching_indices(alice_bases, eav_bases)

    shared_key_alice = utils.get_key(alice_bits, matching_bases_alice_bob)
    shared_key_bob = utils.get_key(bob_bits, matching_bases_alice_bob)
    
    # times where Bob guessed right and Eav wrong
    potential_bit_switch_key = len(list(set(matching_bases_alice_bob) & set(mismatching_bases_eav)))
    # (Bob right and Eav wrong) / (Bob right)
    potential_bit_switch_rate = (potential_bit_switch_key / len(matching_bases_alice_bob)) if len(matching_bases_alice_bob) else 0

    bit_switches_keys = len(utils.mismatching_indices(shared_key_alice, shared_key_bob))
    actual_bit_switch_rate = (bit_switches_keys / potential_bit_switch_key) if potential_bit_switch_key else 0

    error_rate = utils.calculate_error_rate(shared_key_alice, shared_key_bob)

    return shared_key_alice, shared_key_bob, potential_bit_switch_rate, actual_bit_switch_rate, error_rate

def average_sim(n_simulations, n_qubits):
    potential_bit_switch_rate_mean = 0
    actual_bit_switch_rate_mean = 0
    error_rate_mean = 0

    for _ in range(n_simulations):
        alice_bases, alice_bits, bob_bases, bob_bits, eav_bases = simulate_BB84(n_qubits)
        _, _, potential_bit_switch_rate, actual_bit_switch_rate, error_rate = get_statistic(alice_bases, alice_bits, bob_bases, bob_bits, eav_bases)
        potential_bit_switch_rate_mean += potential_bit_switch_rate
        actual_bit_switch_rate_mean += actual_bit_switch_rate
        error_rate_mean += error_rate

    potential_bit_switch_rate_mean /= n_simulations
    actual_bit_switch_rate_mean /= n_simulations
    error_rate_mean /= n_simulations

    return potential_bit_switch_rate_mean, actual_bit_switch_rate_mean, error_rate_mean

