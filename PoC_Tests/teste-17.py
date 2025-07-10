import random

# Define weights for each scoring variable
weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.72392,
    "ja4l_hash": 0.10282,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.35828,  # Restored weight for significant changes
    "user_agent": 0.29481,
    "source_ipv4": 0.14992
}

# Define a variation threshold for applying the volatility penalty
variation_threshold_adjusted = 0.200
volatility_penalty = 0.64

# Function to calculate score with adjusted logic for minor content-length changes
def calculate_score(deviations, weights, last_score, variation_threshold_adjusted, volatility_penalty):
    # Calculate the score considering deviations and weights
    score = sum(deviations[var] * weights[var] for var in deviations)
    
    # Apply the volatility penalty if necessary
    if last_score > 0 and abs(score - last_score) / last_score > variation_threshold_adjusted:
        score *= (1 + volatility_penalty)
    
    return score

# Simulate 17 random requests
last_score = 0.1  # Initialize with a small non-zero value
scores = []

for i in range(200):
    # Generate deviations for the scenario
    deviations = {
        "ja3_hash": 0,
        "ja4_hash": 0,
        "ja4h_hash": random.uniform(1, 1) if i == 16 else 0.01,  # Significant change for one request
        "ja4l_hash": 0,
        "get_header_signature": 0,
        "post_header_signature": random.uniform(0.5, 0.75) if i < 5 else 0.01,
        "content_length": random.uniform(0.01, 0.03),  # Minor changes for all requests
        "user_agent": random.uniform(0.5, 0.75) if i < 5 else 0.01,
        "source_ipv4": random.uniform(0.5, 0.75) if i < 5 or i == 16 else 0.01,  # Minimal impact unless specified    
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


