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


