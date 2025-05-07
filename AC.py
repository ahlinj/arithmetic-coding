# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:13:12 2025

@author: Jaka
"""

import decimal
import random


from arithmetic_encoder_core import encode
from arithmetic_decoder_core import decode

def create_random_sequence_from_prob(alphabet_chars, length, prob):
    return ''.join(random.choices(alphabet_chars, weights=prob, k=length))


if __name__ == '__main__':
    # --- Configuration ---
    decimal.getcontext().prec = 150 # Precision for Decimal calculations
    
    alphabet = ['a', 'b', 'c', 'd']
    prob_dist = [0.5, 0.3, 0.1, 0.1]
    seq_len = 100
    test_sequence = create_random_sequence_from_prob(alphabet, seq_len, prob_dist)

    print(f"Original Sequence ({len(test_sequence)} chars): '{test_sequence}'")

    # --- Encoding ---
    print("\nEncoding...")
    encoded_low, encoded_high = encode(test_sequence, alphabet)
    print(f"Encoded Interval: [{encoded_low}, {encoded_high})")
    print(f"Interval Width:   {encoded_high - encoded_low}")

    # --- Midpoint value to decode ---

    value_to_decode = encoded_low + (encoded_high - encoded_low) / 2

    # --- Decoding ---
    print("\nDecoding...")
    decoded_sequence = decode(value_to_decode, len(test_sequence), alphabet)
    print(f"Decoded Sequence ({len(decoded_sequence)} chars): '{decoded_sequence}'")

    # --- Verification ---
    if test_sequence == decoded_sequence:
        print("\nSUCCESS: Decoded sequence matches the original.")
    else:
        print("\nERROR: Decoded sequence does NOT match the original.")
        # Optional: Find first mismatch point for debugging
        for i in range(min(len(test_sequence), len(decoded_sequence))):
            if test_sequence[i] != decoded_sequence[i]:
                print(f"First mismatch at index {i}: Original='{test_sequence[i]}', Decoded='{decoded_sequence[i]}'")
                print(f"Original context: ...{test_sequence[max(0, i-10):i+10]}...")
                print(f"Decoded context:  ...{decoded_sequence[max(0, i-10):i+10]}...")
                break
        if len(test_sequence) != len(decoded_sequence):
             print(f"Length mismatch: Original={len(test_sequence)}, Decoded={len(decoded_sequence)}")