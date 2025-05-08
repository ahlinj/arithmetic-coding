# -*- coding: utf-8 -*-
"""
Created on Wed May  7 11:13:12 2025

@author: Jaka
"""

from decimal import Decimal, getcontext
import random

from arithmetic_encoder_core import encode
from arithmetic_decoder_core import decode

from huffman_encoder_core import huf_encode


def create_random_sequence_from_prob(alphabet_chars, length, prob):
    return ''.join(random.choices(alphabet_chars, weights=prob, k=length))


def interval_to_binary_decimal(low: Decimal, high: Decimal):
    binary = ""
    value = Decimal(0)
    factor = Decimal('0.5')

    while True:
        mid = value + factor

        if mid < low:
            binary += '1'
            value = mid
        elif mid >= high:
            binary += '0'
        else:
            binary += '1'
            value = mid
            break

        factor /= 2
    return binary


if __name__ == '__main__':
    # --- Configuration ---
    getcontext().prec = 150  # global Decimal precision

    alphabet = ['a', 'b', 'c', 'd']
    prob_dist = [0.5, 0.3, 0.1, 0.1]
    seq_len = 100
    test_sequence = create_random_sequence_from_prob(alphabet, seq_len, prob_dist)

    print(f"Original Sequence ({len(test_sequence)} chars): '{test_sequence}'")

    # --- AC Encoding ---
    print("\nEncoding...")
    encoded_low, encoded_high = encode(test_sequence, alphabet)
    print(f"Encoded Interval: [{encoded_low}, {encoded_high})")
    print(f"Interval Width:   {encoded_high - encoded_low}")
    binary = interval_to_binary_decimal(encoded_low, encoded_high)
    print(f"Binary representation ({len(binary)} bits): {binary}")
    
    # --- Huffman Encoding ---
    print("\nEncoding (Huffman)...")
    huf_binary = huf_encode(test_sequence)
    print(f"Binary representation (Huffman) ({len(huf_binary)} bits): {huf_binary}")
    
    # --- Binary Sequence Length Comparison
    print(f"Arithmetic Encoding Binary Sequence Length: {len(binary)}")
    print(f"Huffman Encoding Binary Sequence Length: {len(huf_binary)}")
    len_dif = len(binary)-len(huf_binary)
    print(f"Length Difference: {len_dif}")

    # --- AC Decoding ---
    value_to_decode = encoded_low + (encoded_high - encoded_low) / 2
    print("\nDecoding...")
    decoded_sequence = decode(value_to_decode, len(test_sequence), alphabet)
    print(f"Decoded Sequence ({len(decoded_sequence)} chars): '{decoded_sequence}'")

    # --- AC Verification ---
    if test_sequence == decoded_sequence:
        print("\nSUCCESS: Decoded sequence matches the original.")
    else:
        print("\nERROR: Decoded sequence does NOT match the original.")
        for i in range(min(len(test_sequence), len(decoded_sequence))):
            if test_sequence[i] != decoded_sequence[i]:
                print(f"First mismatch at index {i}: Original='{test_sequence[i]}', Decoded='{decoded_sequence[i]}'")
                print(f"Original context: ...{test_sequence[max(0, i-10):i+10]}...")
                print(f"Decoded context:  ...{decoded_sequence[max(0, i-10):i+10]}...")
                break
        if len(test_sequence) != len(decoded_sequence):
            print(f"Length mismatch: Original={len(test_sequence)}, Decoded={len(decoded_sequence)}")
