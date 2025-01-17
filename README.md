# README

## Overview

This project simulates the BB84 quantum key distribution protocol, demonstrating how quantum mechanics can be used to securely exchange cryptographic keys. The simulation also includes an optional "eavesdropping" feature to illustrate the impact of a third party attempting to intercept the communication.

## How to Use

1. **Open the Script**  
   Open the `main.py` file in your preferred code editor.

2. **Configure Eavesdropping**  
   Locate the variable `eavesdropping_enabled` near the top of the `main()` function:
   - Set to `True` to simulate eavesdropping (Eve intercepts and manipulates the qubits).
   - Set to `False` for a secure communication scenario.

3. **Run the Script**  
   Execute the script using the following command:
   eavesdropping_enabled = True
    python main.py



4. **Optional Simulation**  
To run multiple simulations and calculate average metrics, call the `main_sim()` function instead.

## Output Explanation

1. **Steps 1-3: Preparing, Eavesdropping, and Measuring**  
The simulation outputs the bases used by Alice, Bob, and Eve (if enabled) and compares their results. You will see a table showing:
- Alice's, Eve's, and Bob's bases.
- Alice's and Bob's bit sequences.

2. **Step 4: Analyzing Matching and Mismatching Bases**  
The script identifies:
- Indices where Alice's and Bob's bases match (key generation points).
- Indices where Eve's guesses are incorrect.

3. **Step 5: Calculating Statistics**  
The program calculates:
- The potential bit-switch rate (cases where Bob guesses correctly and Eve does not).
- The actual bit-switch rate in the generated keys.
- The total error rate in the keys exchanged between Alice and Bob.

4. **Step 6: Error Rate Analysis**  
If the error rate in the published portion of the key exceeds a threshold (e.g., 20%), eavesdropping is likely. Otherwise, Alice and Bob proceed with the remaining unpublished parts of the key.

5. **Final Output**  
Depending on the error rates, the script outputs:
- The private keys of Alice and Bob.
- Any detected eavesdropping or the finalized secure keys.

## Notes

- The parameter `n_qubits` determines the number of qubits exchanged during the simulation. You can adjust it for different scenarios.
- For detailed analysis and debugging, modify the functions in the `alice.py`, `bob.py`, `eav.py`, `utils.py`, and `simulate.py` modules.

## Example Command

To simulate secure communication without eavesdropping:
```python
eavesdropping_enabled = False
python main.py
