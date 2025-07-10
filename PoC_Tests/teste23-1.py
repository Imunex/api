# Re-defining the entire code setup including the calculate_score function for the retest

# Re-defining updated_weights and sensitivity_thresholds with the last adjustments
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

sensitivity_thresholds = {
    "ja3_hash": 0.8,
    "ja4_hash": 0.8,
    "ja4h_hash": 0.8,
    "ja4l_hash": 0.8,
    "get_header_signature": 0.8,
    "post_header_signature": 0.8,
    "content_length": 0.8,  
    "user_agent": 0.8,
    "source_ipv4": 0.8
}

volatility_threshold = 0.230
volatility_penalty = 1.4
minimum_deviation = 0.01

# Defining the calculate_score function with the necessary adjustments
def calculate_score(deviations, last_score, weights, thresholds, penalty, min_deviation):
    score = 0
    for var, deviation in deviations.items():
        # Apply minimum deviation to ensure score is never zero
        adjusted_deviation = max(deviation, min_deviation)
        # Calculate score only for significant changes
        if adjusted_deviation > thresholds[var]:
            score += adjusted_deviation * weights[var]
        else:
            score += min_deviation * weights[var]  # Apply minimum impact for non-significant changes
    
    # Apply volatility penalty based on the relative change
    relative_change = abs(score - last_score) / last_score if last_score > 0 else 0
    if relative_change > volatility_threshold:
        score *= penalty

    return score

# Resetting the last score for the final test and simulate the scenario with 23 requests
scores_scenario_final_test = []
last_score_scenario_final_test = 0.0

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

    current_score = calculate_score(deviations, last_score_scenario_final_test, updated_weights, sensitivity_thresholds, volatility_penalty, minimum_deviation)
    scores_scenario_final_test.append(current_score)
    last_score_scenario_final_test = current_score

scores_scenario_final_test
