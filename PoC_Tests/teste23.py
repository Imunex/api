# scenario: 
#
# 23 random requests where:
# four requests changed the source_ipv4, user-agent and post_header_signature;
# all requests changed few bytes the content-length 
# two request changed the source_ipv4, user-agent and get_header_signature
# One request changed the ja4h and source_ipv4


import random

# Updated weights for each variable
updated_weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.6739,
    "ja4l_hash": 0.1028,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.35828,  
    "user_agent": 0.29481,
    "source_ipv4": 0.14992
}

# Sensitivity thresholds for each variable
sensitivity_thresholds = {
    "ja3_hash": 0.24855,
    "ja4_hash": 0.68774,
    "ja4h_hash": 1.84918,
    "ja4l_hash": 0.14758,
    "get_header_signature": 0.19284,
    "post_header_signature": 0.19664,
    "content_length": 0.12485,  
    "user_agent": 0.11837,
    "source_ipv4": 0.12938
}

volatility_threshold = 0.130
volatility_penalty = 1.4
minimum_deviation = 0.01

# Function to calculate scores with adjustments for 4-digit decimal scale
def calculate_score_decimal_scale(deviations, last_score, weights, thresholds, penalty, min_deviation):
    score = 0
    for var, deviation in deviations.items():
        adjusted_deviation = max(deviation, min_deviation)
        if adjusted_deviation > thresholds[var]:
            score += adjusted_deviation * weights[var]
        else:
            score += min_deviation * weights[var]
    
    relative_change = abs(score - last_score) / last_score if last_score > 0 else 0
    if relative_change > volatility_threshold:
        score *= penalty

 # Ensure score never goes below 0.1999
    score = max(round(score, 4), 0.1)

    return score


# Simulating the scoring for 23 requests with adjusted sensitivity thresholds
final_scores = []
last_score = 0.0
for i in range(23):
    deviations = {
        "ja3_hash": random.uniform(0.1, 0.2) if i in [5, 18, 19] else minimum_deviation,
        "ja4_hash": minimum_deviation,
        "ja4h_hash": random.uniform(0.1, 0.2) if i == 22 else minimum_deviation,
        "ja4l_hash": minimum_deviation,
        "get_header_signature": random.uniform(0.1, 0.2) if i in [18, 19] else minimum_deviation,
        "post_header_signature": random.uniform(0.1, 0.2) if i < 4 else minimum_deviation,
        "content_length": random.uniform(0.05, 0.15),
        "user_agent": random.uniform(0.1, 0.2) if i in [0, 1, 2, 3, 18, 19] else minimum_deviation,
        "source_ipv4": random.uniform(0.1, 0.2) if i in [0, 1, 2, 3, 18, 19, 22] else minimum_deviation
    }

    current_score = calculate_score_decimal_scale(deviations, last_score, updated_weights, sensitivity_thresholds, volatility_penalty, minimum_deviation)
    final_scores.append(current_score)
    last_score = current_score

# Print each calculated score on a new line
for score in final_scores:
    print(f"{score}")
