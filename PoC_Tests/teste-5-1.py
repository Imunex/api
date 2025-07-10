import random

# Define the updated weights for each variable
weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.71499,
    "ja4l_hash": 0.10284,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.35828,
    "user_agent": 0.29481,
    "source_ipv4": 0.14992
}

# Define the volatility penalty factor and the minimum deviation
volatility_penalty = 1.5
minimum_deviation = 0.1  # Ensures deviations are never set to 0.0

# Adjust the variation_threshold for the simulation
variation_threshold_adjusted = 0.225

# Initialize a placeholder for the last score to simulate consecutive requests
last_simulated_score = 0.0

# Simulate 5 random requests with changes in source_ipv4, ja3_hash, and user-agent
simulated_scores = []
for i in range(50):
    # Generate random deviations for source_ipv4, ja3_hash, and user-agent, ensuring they are never zero
    deviations = {
        "ja3_hash": random.uniform(0.1, 0.2) if i in [5, 18, 19] else minimum_deviation,
        "ja4_hash": minimum_deviation,
        "ja4h_hash": random.uniform(0.1, 0.15) if i == 35 else minimum_deviation,
        "ja4l_hash": minimum_deviation,
        "get_header_signature": random.uniform(0.1, 0.2) if i in [18, 19] else minimum_deviation,
        "post_header_signature": random.uniform(0.1, 0.2) if i < 4 else minimum_deviation,
        "content_length": random.uniform(0.05, 0.15),
        "user_agent": random.uniform(0.1, 0.2) if i in [0, 1, 2, 3, 18, 19] else minimum_deviation,
        "source_ipv4": random.uniform(0.1, 0.2) if i in [0, 1, 2, 3, 18, 19, 22] else minimum_deviation
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

relative_change = abs(current_score - last_simulated_score) / last_simulated_score if last_simulated_score != 0 else 0
if relative_change > variation_threshold_adjusted:
    current_score *= (1 + volatility_penalty)
simulated_scores.append(current_score)

simulated_scores

for score in simulated_scores:
    print(f"{score}")

