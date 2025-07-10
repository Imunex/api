# Example deviations for each variable (in a real scenario, these would be calculated based on actual data)
deviations = {
    "ja3_hash": 0.12,  # 10% deviation
    "ja4_hash": 0.25,
    "ja4h_hash": 0.56,
    "ja4l_hash": 0.20,
    "get_header_signature": 0.15,
    "post_header_signature": 0.15,
    "content_length": 0.5,
    "user_agent": 0.24,
    "source_ipv4": 0.19
}

# Weights for each variable
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

# Calculate the weighted score
score = sum(deviations[var] * weights[var] for var in deviations)

# Add the score to the JSON data
json_data = {
    "ja3_hash": "773906b0efdefa24a7f2b8eb6985bf37",
    "ja4_hash": "t13i2012h1_1e948f1242c7_d9433a03ec64",
    "ja4h_hash": "ge11cn060000_4e59edc1297a_4da5efaf0cbd",
    "ja4l_hash": "5191_42_45014",
    "get_header_signature": "1a93b037806d72961f17aa649841b9cbb70f1281428e3235128b9e24cde69fe5",
    "post_header_signature": "953eea58fdd34dfe4f0760f131a78cab9abdcab2800a5c5569eb418e01d97c7e",
    "user_agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3.1 Mobile/15E148 Safari/604.1",
    "accept": "*/*",
    "accept_encoding": "gzip, deflate, br",
    "accept_language": "en-US,en;q=0.9",
    "connection": "keep-alive",
    "content_length": "384",
    "host": "api.devtest.com",
    "source_ipv4": "172.16.0.1",
    "client_score": score
}

print(json_data)