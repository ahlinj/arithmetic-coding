# -*- coding: utf-8 -*-

import decimal
from collections import Counter

def _get_laplace_probabilities_for_encoding(previous_sequence, alphabet):
    alphabet_size = len(alphabet)
    seq_len = len(previous_sequence)
    counts = Counter(previous_sequence)
    
    denominator = decimal.Decimal(seq_len + alphabet_size)

    # Handle initial case (empty previous_sequence) or empty alphabet (less likely for valid input)
    if denominator == 0: # Only if alphabet_size and seq_len are 0
        if alphabet_size > 0: # seq_len is 0, initial step
            denominator = decimal.Decimal(alphabet_size)
        else: # Should not happen with valid alphabet
            return [] 

    probabilities_dist = []
    current_cumulative_prob = decimal.Decimal(0)

    for char_val in alphabet:
        char_count = counts[char_val]
        prob = (decimal.Decimal(char_count + 1)) / denominator
        
        probabilities_dist.append({
            "char": char_val,
            "prob": prob,
            "cum_low": current_cumulative_prob 
        })
        current_cumulative_prob += prob
        
    return probabilities_dist

def encode(sequence, alphabet):
    low = decimal.Decimal(0.0)
    current_interval_width = decimal.Decimal(1.0)

    for i, current_char_to_encode in enumerate(sequence):
        previous_sequence_context = sequence[0:i]
        
        prob_distribution = _get_laplace_probabilities_for_encoding(
            previous_sequence_context, alphabet
        )
        
        char_prob_info = next(
            p_info for p_info in prob_distribution if p_info["char"] == current_char_to_encode
        )
        # Assumes current_char_to_encode is always in alphabet and model provides for it.
        
        low += current_interval_width * char_prob_info["cum_low"]
        current_interval_width *= char_prob_info["prob"]
        
    high = low + current_interval_width
    return low, high