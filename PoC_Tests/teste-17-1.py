import json
import random

def calculate_score(deviations, weights, content_length_change_threshold=0.05):
    # Adjust the content_length deviation based on a significant change threshold
    content_length_deviation = deviations["content_length"]
    if content_length_deviation < content_length_change_threshold:
        deviations["content_length"] = 0  # Ignore minor changes
    
    # Calculate the score
    score = sum(deviations[var] * weights[var] for var in deviations)
    return score

# Weights for each variable, focusing on minimizing the impact of slight content-length changes
weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.77399,
    "ja4l_hash": 0.1028,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.35828,  # Restored weight for significant changes
    "user_agent": 0.29481,
    "source_ipv4": 0.24992
}

# Simulating the scenario with updated logic to minimize the impact of slight content-length changes
simulated_scores = []
for i in range(100):
    deviations = {
        "source_ipv4": random.uniform(0.5, 0.75) if i < 5 or i == 16 else 0,
        "user_agent": random.uniform(0.5, 0.75) if i < 5 else 0,
        "post_header_signature": random.uniform(0.5, 0.75) if i < 5 else 0,
        "content_length": random.uniform(0.01, 0.03),  # Minor change for all requests
        "ja4h_hash": random.uniform(0.5, 0.75) if i == 16 else 0  # Significant change for the last request
    }

    current_score = calculate_score(deviations, weights, 0.05)
    simulated_scores.append(current_score)

print(simulated_scores)