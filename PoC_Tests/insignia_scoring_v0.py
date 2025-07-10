import random

# Define updated weights for the scoring system
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

# Volatility settings
volatility_threshold = 0.230
volatility_penalty = 1.4
minimum_deviation = 0.01

# Function to calculate scores, apply minimum deviations, and the volatility penalty
def calculate_and_adjust_score(deviations, weights, last_score, threshold, penalty):
    for var in deviations.keys():
        deviations[var] = max(deviations[var], minimum_deviation)
    
    score = sum(deviations[var] * weights[var] for var in deviations)
    
    relative_change = abs(score - last_score) / last_score if last_score > 0 else 0
    if relative_change > threshold:
        score *= penalty
    
    return score

# Simulate scoring for 23 random requests based on scenario conditions
scenario_scores = []
last_score = 0.0

for i in range(23):
    deviations = {
        "ja3_hash": random.uniform(0.5, 0.75) if i == 5 else minimum_deviation,
        "ja4_hash": minimum_deviation,
        "ja4h_hash": random.uniform(0.5, 0.75) if i == 22 else minimum_deviation,
        "ja4l_hash": minimum_deviation,
        "get_header_signature": random.uniform(0.5, 0.75) if 18 <= i <= 19 else minimum_deviation,
        "post_header_signature": random.uniform(0.5, 0.75) if i < 4 else minimum_deviation,
        "content_length": random.uniform(0.01, 0.03),
        "user_agent": random.uniform(0.5, 0.75) if i < 4 or 18 <= i <= 19 else minimum_deviation,
        "source_ipv4": random.uniform(0.5, 0.75) if i < 4 or 18 <= i <= 19 or i == 22 else minimum_deviation
    }

    current_score = calculate_and_adjust_score(deviations, updated_weights, last_score, volatility_threshold, volatility_penalty)
    scenario_scores.append(current_score)
    last_score = current_score


# Output the scores for review
for score in scenario_scores:
print(score)
