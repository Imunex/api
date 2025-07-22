from api.models.models import User, Scores, Devices 
from api.logs import GenerateLogs
from api.algorithms.data_analisis import analyse_ja4h
LOGGER = GenerateLogs


def weights_gen():
    return {
        "ja3_hash": 0.49921,
        "ja4_hash": 0.38823,
        "ja4h_hash": 0.65392,
        # "ja4l_hash": 0.10282,
        # "get_header_signature": 0.24534,
        # "post_header_signature": 0.25912,
        "content_length": 0.26832,  # Restored weight for significant changes
        "user_agent": 0.46181,
        "source_ipv4": 0.24992
    }


def calculate_score(deviations, weights, last_score, variation_threshold_adjusted, volatility_penalty):
    # Calculate the score considering deviations and weights
    score = sum(deviations[var] * weights[var] for var in deviations)

    # Apply the volatility penalty if necessary
    if last_score > 0 and abs(score - last_score) / last_score > variation_threshold_adjusted:
        score *= (1 + volatility_penalty)

    return score



def generate_scores(data, score: Scores):
    parsed_old_len = int(50 if score.content_length is None else score.content_length)
    parsed_len = int(50 if data.get("content_length") is None else data.get("content_length"))
    user_agent_score = 0
    if data.get("user_agent") != score.user_agent:
        user_agent_score = 0.415
    ja4h_score = analyse_ja4h(score.ja4h, data.get("ja4h"))
    return{
            # Medium changes requests
            "ja3_hash": 0.731 if data.get("ja3") != score.ja3 else 0.01,
            # Minor changes requests
            "ja4_hash": 0.4 if data.get("ja4") != score.ja4 else 0.01,
            # Significant change request
            "ja4h_hash": ja4h_score if data.get("ja4h") != score.ja4h else 0.01,
            # "ja4l_hash": random.uniform(0.01, 0.03) if data["ja4l"] != device.ja4l else 0.01,                                # Minor changes requests
            # "get_header_signature": random.uniform(0.3, 0.45) if data["get_header_signature"] != device.get_header_signature else 0.01,                      # Medium changes requests
            # Medium changes requests
            # "post_header_signature": 0.350 if data.get("post_header_signature") != score.post_header_signature else 0.01,
            # Minor changes requests
            "content_length": 0.232 if not (parsed_len-50 <= int(parsed_old_len) <= parsed_len+50 ) else 0.01,
            # Medium changes requests
            "user_agent": user_agent_score if data.get("user_agent") != score.user_agent else 0.01,
            # Minimal impact unless specified
            "source_ipv4": 0.231 if data.get("source_ipv4") != score.source_ipv4 else 0.01
        }

def pontuation(deviations, weights, device):
    current_score_enhanced = sum(
        deviations[var] * weights[var] for var in deviations if var != "content_length" or deviations["content_length"] > 0.04
    )
    last_score = Scores.objects.filter(device=device).latest("created_at").score if Scores.objects.filter(device=device).last() else 0.1
    current_score = calculate_score(
        deviations, weights, last_score, variation_threshold_adjusted, volatility_penalty)
    
    return current_score, current_score_enhanced, last_score

def define_score_enhanced(device: Devices, data, is_activation=False):
    score = Scores.objects.filter(device=device, is_safe = True).order_by("-created_at").first()
    weights = weights_gen()
    if not score:
        return 99, 99, ["Not Score"]
    deviations = generate_scores(data, score)
    offensors= []
    for key, value in deviations.items():
        if value > 0.01:
            offensors.append(key)

    
    data["source"] = "API Call"

    if is_activation: # If user is requesting activation
        deviations["content_length"] = 0.01 # Set low deviation to content_length
        if deviations["source_ipv4"] == 0.01 and deviations["ja4_hash"]==0.01: # check if source_ipv4 AND ja4_hash have changed
            deviations["ja4h_hash"] = 1.25 # If source_ipv4 AND ja4_hash have NOT changed set the ja4h_hash to HIGH
    
    current_score, current_score_enhanced, last_score = pontuation(deviations, weights, device)

    if last_score > 0 and abs(current_score_enhanced - last_score) / last_score > variation_threshold_adjusted:
        current_score_enhanced *= (1 + volatility_penalty)

    return current_score, current_score_enhanced, offensors

variation_threshold_adjusted = 0.200
volatility_penalty = 0.64



def calculate_permission(request, data, user: User, action="Login", is_activation=False):
    verified = not is_activation
    devices = user.devices.filter(verified=verified)
    scores = [[100, None, "Base"]]
    score_enhanced = [100]
    for device in devices:
        current_score, current_score_enhanced, offensors = define_score_enhanced(device, data, is_activation)
        scores.append([current_score, device, offensors])
        score_enhanced.append(current_score_enhanced)
    lower_device = min(scores, key=lambda x: x[0])[1]
    lower_offensors =  min(scores, key=lambda x: x[0])[2]
    lower_score = min(scores, key=lambda x: x[0])[0]
    lower_score_enhanced = min(score_enhanced)
    is_safe = False
    if lower_score < 0.5 :
        is_safe = True

    LOGGER(request, "INFO", action).write_log(f"""Fingerprint calculated for user {'****' + user.email[4:]} SCORE: {lower_score}, 
                                              enhanced score is {lower_score_enhanced}, ja4: {data.get("ja4")}, 
                                              ja4h: {data.get("ja4h")}, ja3: {data.get("ja3")},
                                              post_header_signature: {data.get("post_header_signature")}, 
                                              content_length: {data.get("content_length")}, source_ipv4: {data.get("source_ipv4")}, 
                                              user_agent: {data.get("user_agent")}""")
    
    Scores.objects.create(is_safe=is_safe, device=lower_device, score=lower_score, current_score_enhanced=lower_score_enhanced, ja4=data.get("ja4"), ja4h=data.get("ja4h"),
                        ja3=data.get("ja3"), reason=lower_offensors, #post_header_signature=data.get("post_header_signature"),
                        content_length=data.get("content_length"), source_ipv4=data.get("source_ipv4"), user_agent=data.get("user_agent"), source=data.get("source", "API Call"))

        # request.headers.get('Cloudfront-Viewer-Country-Region-Name', None)
    if lower_score > 1:
        return False, lower_offensors, lower_score, lower_device
    return True, None, lower_score, lower_device
