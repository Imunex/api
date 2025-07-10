#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module Name: insignia_scoring.py
Description: This script demonstrates how to structure a scoring method based in artificial data, 
             aiming to simulate the requests from a hypothetical HTTPS client, once the requests are 
             handled by the HTTPS web server we can use the fingerprints ja3, ja4, ja4h, ja4l and 
             header signatures including other headers from the client's request. 
             The purpose of this script is researching in identify behavior anomaly in HTTPS requests, 
             using a simple mathematical model with weights, deviations, variation thresholds and volatility of the variable's behavior.
Author: Tiago Flores a.k.a hanaga
Date: 2024-03-01
License: MIT License
Version: 1.0.0
Dependencies: random
Usage: python insignia_scoring.py

"""
import random

# Define weights for each scoring variable
weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.52392,
    "ja4l_hash": 0.10282,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.45828,  # Restored weight for significant changes
    "user_agent": 0.26481,
    "source_ipv4": 0.14992
}

# Define a variation threshold for applying the volatility penalty
variation_threshold_adjusted = 0.200
volatility_penalty = 0.64

# Calculate score with adjusted logic for minor content-length changes
def calculate_score(deviations, weights, last_score, variation_threshold_adjusted, volatility_penalty):
    # Calculate the score considering deviations and weights
    score = sum(deviations[var] * weights[var] for var in deviations)
    
    # Apply the volatility penalty if necessary
    if last_score > 0 and abs(score - last_score) / last_score > variation_threshold_adjusted:
        score *= (1 + volatility_penalty)
    
    return score


last_score = 0.1  # Initialize with a small non-zero value
scores = []

# Simulate x random requests in range(x)
for i in range(100000):
    # Generate deviations for the scenario

    # actual scenario: Adjusting the randominzation to increase/decrease the dificulty of detections.
    deviations = {
        "ja3_hash": random.uniform(0.5, 0.75) if i in [377, 4999, 6790, 7943, 1316, 4020] else 0.01,    # Medium changes requests
        "ja4_hash": random.uniform(0.01, 0.03) if i < 100000 else 0.01,                                 # Minor changes requests
        "ja4h_hash": random.uniform(1, 1) if i in [4506, 6199, 9319, 8352, 5600, 3423] else 0.01,       # Significant change request
        "ja4l_hash": random.uniform(0.01, 0.03) if i < 100000 else 0.01,                                # Minor changes requests
        "get_header_signature": random.uniform(0.3, 0.45) if i < 100000 else 0.01,                      # Medium changes requests
        "post_header_signature": random.uniform(0.5, 0.75) if i < 100000 else 0.01,                     # Medium changes requests
        "content_length": random.uniform(1, 1) if i in [1111, 2222, 3333, 4444, 11111, 55555] else 0.01,                           # Minor changes requests
        "user_agent": random.uniform(0.5, 0.75) if i < 100000 else 0.01,                                # Medium changes requests
        "source_ipv4": random.uniform(0.5, 0.75) if i in [8950, 90, 7654, 315, 2651, 476] else 0.01     # Minimal impact unless specified    
    }


    current_score_enhanced = sum(
        deviations[var] * weights[var] for var in deviations if var != "content_length" or deviations["content_length"] > 0.04
    )
    
    current_score = calculate_score(deviations, weights, last_score, variation_threshold_adjusted, volatility_penalty)
    
    if i > 0 and last_score > 0 and abs(current_score_enhanced - last_score) / last_score > variation_threshold_adjusted:
        current_score_enhanced *= (1 + volatility_penalty)
    
    # Print the deviation values for the current request
    print(f"Request {i+1} Deviations:")
    for key, value in deviations.items():
        print(f"  {key}: {value:.3f}")
    print(f"  Calculated Score: {current_score:.3f}\n")
    
    #simulated_scores_final_test.append(current_score_enhanced)
    #last_simulated_score_final = current_score_enhanced if current_score_enhanced > 0 else last_simulated_score_final

    
    # Calculate the score for each request
    scores.append(current_score)
    last_score = current_score if current_score > 0 else last_score # Update last score for the next iteration
   

# print scores

for index, score in enumerate(scores):
    #print("Request score: ", score)
    if score >= 1.0: 
        print(f"Abnormal detection in request {index}: {score}\n")


#  Look for the Significant change request; Change the scenario and re-run the script.
#  Ex. looking the Significant change request
#  python3 insignia_scoring_v1.py | grep "Abnormal" | grep -e "request 4506\|request 6199\|request 8352\|request 5600\|request 9319\|request 3423" --color
