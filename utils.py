from bitarray import bitarray
from bitarray.util import ba2int, int2ba
import math

def matching_indices(ar1, ar2):
    return [i for i, (a, b) in enumerate(zip(ar1, ar2)) if a == b]

def mismatching_indices(ar1, ar2):
    return [i for i, (a, b) in enumerate(zip(ar1, ar2)) if a != b]

def get_key(bits, matching_bases):
    return [bits[i] for i in matching_bases]

def calculate_error_rate(alice_key, bob_key):
    errors = sum(a != b for a, b in zip(alice_key, bob_key))
    error_rate = errors / len(alice_key) if alice_key else 0
    return error_rate

import math

def calculate_parity_bits(data_bits_length):
    """
    Calculate the minimum number of parity bits required for a given length of data bits
    such that the Hamming code can encode the data correctly.
    """
    m = 0
    while (1 << m) < (data_bits_length + m + 1):
        m += 1
    return m

def hamming_encode(data_bits):
    """
    Hamming code to encode data bits with error correction capability.
    - `data_bits`: Input data bits as a list of integers (0s and 1s).
    
    Returns:
    - `encoded_bits`: Encoded bit sequence as a list of integers.
    """
    m = calculate_parity_bits(len(data_bits))  # Calculate the number of parity bits
    n = len(data_bits) + m  # Total number of bits (data + parity bits)

    # Initialize encoded bits with 0
    encoded_bits = [0] * n

    # Set data bits at positions that are not powers of 2 (parity bit positions)
    data_index = 0
    for i in range(1, n + 1):
        if (i & (i - 1)) != 0:  # Not a power of 2 (parity bit positions)
            encoded_bits[i - 1] = data_bits[data_index]
            data_index += 1

    # Calculate parity bits
    for i in range(m):
        parity_index = (1 << i) - 1  # Parity bit position (0-based index)
        parity = 0
        for j in range(n):
            if (j + 1) & (1 << i):  # Check if the bit is involved in this parity
                parity ^= encoded_bits[j]
        encoded_bits[parity_index] = parity
    
    return encoded_bits



def hamming_decode(encoded_bits):
    """
    Hamming decode to recover the data bits from the encoded bits.
    - `encoded_bits`: The encoded Hamming code (including data and parity bits).
    
    Returns:
    - `decoded_bits`: The decoded data bits (after error correction).
    - `error_position`: The position of the detected error, or 0 if no error is detected.
    """
    n = len(encoded_bits)
    m = int(math.log2(n + 1))  # Calculate the number of parity bits (m)
    
    # Check for parity errors
    error_position = 0
    
    # Check all parity bits
    for i in range(m):
        parity_index = (1 << i) - 1  # Position of the parity bit (0-based index)
        parity = 0
        
        # Calculate the parity for the current parity bit
        for j in range(n):
            if (j + 1) & (1 << i):  # Check if the bit is involved in this parity
                parity ^= encoded_bits[j]
        
        # If the calculated parity is 1, there is an error at this position
        if parity != 0:
            error_position += (1 << i)
    
    # If error_position is not 0, it means an error was detected
    if error_position > 0:
        print(f"Error detected at position: {error_position}")
        # Correct the error (flip the bit)
        encoded_bits[error_position - 1] ^= 1
    
    # Extract the original data bits (ignore parity bit positions)
    decoded_bits = []
    for i in range(n):
        if (i + 1) & i != 0:  # Skip parity bit positions
            decoded_bits.append(encoded_bits[i])
    
    return decoded_bits, error_position


def unify_keys(key_alice, key_bob):
    """
    Reconcile two keys from Alice and Bob to produce an identical shared key.
    - `key_alice`: Alice's key as a list of bits.
    - `key_bob`: Bob's key as a list of bits.
    
    Returns:
    - `shared_key`: Corrected shared key as a list of bits.
    """
    if len(key_alice) != len(key_bob):
        raise ValueError("Keys must be of equal length.")
    
    # Encode Alice's key
    encoded_alice = hamming_encode(key_alice)
    
    # Encode Bob's key
    encoded_bob = hamming_encode(key_bob)
    
    # Decode and correct errors in Bob's key
    corrected_bob, _ = hamming_decode(encoded_bob)
    
    # Decode Alice's key and verify correctness
    corrected_alice, _ = hamming_decode(encoded_alice)
    
    # Compare the corrected keys
    if corrected_bob != corrected_alice:
        raise ValueError("Reconciliation failed: keys could not be unified.")
    
    return corrected_bob

