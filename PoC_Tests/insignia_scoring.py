import random

# Define the updated weights for each variable
weights = {
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

# Define the volatility penalty factor and the minimum deviation
volatility_penalty = 1.4
minimum_deviation = 0.01  # Ensures deviations are never set to 0.0

# Adjust the variation_threshold for the simulation
variation_threshold_adjusted = 0.230

# Initialize a placeholder for the last score to simulate consecutive requests
last_simulated_score = 0.0

# Simulate 5 random requests with changes in source_ipv4, ja3_hash, and user-agent
simulated_scores = []
for i in range(5):
    # Generate random deviations for source_ipv4, ja3_hash, and user-agent, ensuring they are never zero
    deviations = {
        "ja3_hash": random.uniform(0.5, 0.75),
        "ja4_hash": minimum_deviation,  # Ensure minimum deviation
        "ja4h_hash": minimum_deviation,  # Ensure minimum deviation
        "ja4l_hash": minimum_deviation,  # Ensure minimum deviation
        "get_header_signature": minimum_deviation,  # Ensure minimum deviation
        "post_header_signature": minimum_deviation,  # Ensure minimum deviation
        "content_length": minimum_deviation,  # Ensure minimum deviation
        "user_agent": random.uniform(0.5, 0.75),
        "source_ipv4": random.uniform(0.5, 0.75)
    }

    # Calculate the score for the current request
    current_score = sum(deviations[var] * weights[var] for var in deviations)
    
    # Apply the volatility penalty if the relative change exceeds the adjusted threshold
    if i > 0:  # Skip the penalty application for the first iteration
        relative_change = abs(current_score - last_simulated_score) / last_simulated_score if last_simulated_score != 0 else 0
        if relative_change > variation_threshold_adjusted:
            current_score *= (1 + volatility_penalty)
    
    simulated_scores.append(current_score)
    last_simulated_score = current_score  # Update last score for the next iteration

# Simulate the 6th request with ja4h also changed, ensuring minimum deviations
deviations["ja4h_hash"] = random.uniform(0.5, 0.75)  # Significant change for ja4h
current_score = sum(deviations[var] * weights[var] for var in deviations)
relative_change = abs(current_score - last_simulated_score) / last_simulated_score if last_simulated_score != 0 else 0
if relative_change > variation_threshold_adjusted:
    current_score *= (1 + volatility_penalty)
simulated_scores.append(current_score)

simulated_scores
