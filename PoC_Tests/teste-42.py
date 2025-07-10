import random

# Define weights for each variable
weights = {
    "ja3_hash": 0.45921,
    "ja4_hash": 0.34823,
    "ja4h_hash": 0.6739,
    "ja4l_hash": 0.1028,
    "get_header_signature": 0.24534,
    "post_header_signature": 0.34512,
    "content_length": 0.35828,  # Weight for significant changes
    "user_agent": 0.29481,
    "source_ipv4": 0.14992
}

def calculate_score(deviations):
    """
    Calculate the score for a request based on deviations and weights.
    Ignores minor changes in content_length.
    """
    score = sum(
        deviations[var] * weights[var] for var in deviations if var != "content_length" or deviations["content_length"] > 0.04
    )
    return score

def simulate_request_set():
    """
    Simulate a set of 17 requests, with the last one expected to exhibit abnormal behavior
    due to significant changes in ja4h_hash and source_ipv4.
    """
    scores = []
    for i in range(23):
    
        deviations = {
        "ja3_hash": random.uniform(0.5, 0.75) if i == 5 else 0,
        "ja4_hash": 0,
        "ja4h_hash": random.uniform(0.5, 0.75) if i == 22 else 0,
        "ja4l_hash": 0,
        "get_header_signature": random.uniform(0.5, 0.75) if 18 <= i <= 19 else 0,
        "post_header_signature": random.uniform(0.5, 0.75) if i < 4 else 0,
        "content_length": random.uniform(0.01, 0.03),
        "user_agent": random.uniform(0.5, 0.75) if i < 4 or 18 <= i <= 19 else 0,
        "source_ipv4": random.uniform(0.5, 0.75) if i < 4 or 18 <= i <= 19 or i == 22 else 0
    }
    

        current_score = calculate_score(deviations)
        scores.append(current_score)
    
    # Determine if the abnormal behavior is detected based on the score of the last request
    average_score = sum(scores[:-1]) / max(1, sum(1 for score in scores[:-1] if score > 0))
    is_abnormal_detected = scores[-1] > average_score * 1.5
    return is_abnormal_detected, scores

# Run multiple sets of tests and evaluate detection accuracy
detection_results = [simulate_request_set() for _ in range(12)]
accurate_detections = sum(result[0] for result in detection_results)
accuracy_percentage = (accurate_detections / len(detection_results)) * 100

print(f"Accuracy Percentage: {accuracy_percentage}%")
