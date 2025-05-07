# -*- coding: utf-8 -*-

import decimal
from collections import Counter

def _get_laplace_probabilities_for_decoding(previous_sequence, alphabet):
    alphabet_size = len(alphabet)
    seq_len = len(previous_sequence)
    counts = Counter(previous_sequence)
    
    denominator = decimal.Decimal(seq_len + alphabet_size)

    if denominator == 0:
        if alphabet_size > 0:
            denominator = decimal.Decimal(alphabet_size)
        else:
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

def decode(encoded_value, num_symbols_to_decode, alphabet):
    decoded_symbols_list = []
    current_low = decimal.Decimal(0.0)
    current_interval_width = decimal.Decimal(1.0)

    for _ in range(num_symbols_to_decode):
        context_from_decoded_symbols = "".join(decoded_symbols_list)
        prob_distribution = _get_laplace_probabilities_for_decoding(
            context_from_decoded_symbols, alphabet
        )
        
        # Determine where the encoded_value falls within the current scaled distribution
        # scaled_value = (encoded_value - current_low) / current_interval_width
        # This assumes current_interval_width is not zero.
        target_scaled_value = (encoded_value - current_low) / current_interval_width
        
        char_to_decode_info = None
        for p_info in prob_distribution:
            # Check if target_scaled_value is in [cum_low, cum_low + prob)
            if p_info["cum_low"] <= target_scaled_value < (p_info["cum_low"] + p_info["prob"]):
                 char_to_decode_info = p_info
                 break
        
        # Handle case where target_scaled_value might be exactly at the upper bound of the last symbol
        # due to precision when it should be decoded as the last symbol.
        if char_to_decode_info is None and prob_distribution:
            last_symbol_info = prob_distribution[-1]
            # If target_scaled_value is very close to 1.0 (or the sum of probabilities)
            # and it's within the last symbol's range start.
            if last_symbol_info["cum_low"] <= target_scaled_value <= decimal.Decimal(1) + decimal.Decimal('1e-50'): # Tolerance for 1.0
                char_to_decode_info = last_symbol_info
        
        # Assumes a symbol will always be found if inputs are correct.
        # If char_to_decode_info is still None here, it indicates an issue.
        # For simplicity, we proceed assuming it's found. A robust version would error.
        if char_to_decode_info is None:
             raise Exception(f"Decoder error: Could not find symbol for scaled value {target_scaled_value}. "
                             f"Context: '{context_from_decoded_symbols}', Dist: {prob_distribution}")


        decoded_char = char_to_decode_info["char"]
        decoded_symbols_list.append(decoded_char)
        
        current_low += current_interval_width * char_to_decode_info["cum_low"]
        current_interval_width *= char_to_decode_info["prob"]

    return "".join(decoded_symbols_list)