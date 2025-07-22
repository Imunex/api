import re
def fisrt_part_ja4h(ja4h: str):
    protocol = ja4h[0:2]
    http_version = ja4h[2:4]
    cookie = ja4h[4:5]
    referer = ja4h[5:6]
    headers = ja4h[6:8]
    accept_language = ja4h[8::]
    ja4h_dict = {
        "protocol": protocol,
        "http_version": http_version,
        "cookie": cookie,
        "referer": referer,
        "headers": headers,
        "uri": accept_language
    }
    return ja4h_dict



def analyse_ja4h(old_ja4h: str, new_ja4h: str):
    try:
        old_list = old_ja4h.split("_")
        new_list = new_ja4h.split("_")
        
        old_first_part = fisrt_part_ja4h(old_list[0])
        new_first_part = fisrt_part_ja4h(new_list[0])

        score = 0.0     
        if old_ja4h != new_ja4h:
            score = 0.1
        
        # Define weights for each field based on their importance
        weights = {
            "protocol": 0.3,
            "http_version": 0.2,
            "cookie": 0.2,
            "referer": 0.2,
            "headers": 0.2,
            "uri": 0.3
        }
        
        # Calculate the score based on differences
        score += calculate_difference_score(old_first_part["protocol"], new_first_part["protocol"], weights["protocol"])
        score += calculate_difference_score(old_first_part["http_version"], new_first_part["http_version"], weights["http_version"])
        score += calculate_difference_score(old_first_part["cookie"], new_first_part["cookie"], weights["cookie"])
        score += calculate_difference_score(old_first_part["referer"], new_first_part["referer"], weights["referer"])
        score += calculate_difference_score(old_first_part["headers"], new_first_part["headers"], weights["headers"])
        score += calculate_difference_score(old_first_part["uri"], new_first_part["uri"], weights["uri"])
        
        # Ensure the score is capped at 1
        score = min(score, 0.840)
        
        if old_list[1] != new_list[1]:
            score+= 0.200 
        
        if old_list[2] != new_list[2]:
            score+= 0.100
        
        if old_list[3] != new_list[3]:
            score = 0.100
        
        print("SCORE JA4H GERADO:", score)
        score = min(score, 0.840)

        return score
    except:
        if old_ja4h != new_ja4h:
            return 0.840
        return 0

def first_part_ja4(ja4):
    protocol = ja4[0:1] # t ou q
    tls_version = ja4[1:3] # 1 ou 2
    sni = ja4[3:4] # d to domain, i to ip
    ciphers = ja4[4:6] # number of ciphers
    extensions = ja4[6:8] # number of extensions
    alpn = ja4[8:10] # first alpn value
    ja4_dict = {
        "protocol": protocol,
        "tls_version": tls_version,
        "sni": sni,
        "ciphers": ciphers,
        "extensions": extensions,
        "alpn": alpn
    }
    return ja4_dict


def calculate_difference_score(old_value, new_value, weight):
    if old_value != new_value:
        return weight
    return 0

def analyse_ja4(old_ja4, new_ja4):
    try:
        old_list = old_ja4.split("_")
        new_list = new_ja4.split("_")
        
        old_first_part = first_part_ja4(old_list[0])
        new_first_part = first_part_ja4(new_list[0])
        
        score = 0
        
        # Define weights for each field based on their importance
        weights = {
            "protocol": 0.4,
            "tls_version": 0.3,
            "sni": 0.2,
            "ciphers": 0.1,
            "extensions": 0.1,
            "alpn": 0.1
        }
        
        # Calculate the score based on differences
        score += calculate_difference_score(old_first_part["protocol"], new_first_part["protocol"], weights["protocol"])
        score += calculate_difference_score(old_first_part["tls_version"], new_first_part["tls_version"], weights["tls_version"])
        score += calculate_difference_score(old_first_part["sni"], new_first_part["sni"], weights["sni"])
        score += calculate_difference_score(old_first_part["ciphers"], new_first_part["ciphers"], weights["ciphers"])
        score += calculate_difference_score(old_first_part["extensions"], new_first_part["extensions"], weights["extensions"])
        score += calculate_difference_score(old_first_part["alpn"], new_first_part["alpn"], weights["alpn"])
        
        # Ensure the score is capped at 1
        score = min(score, 0.610)
        
        if old_list[1] != new_list[1]: 
            score += 0.350
        if old_list[2] != new_list[2]:
            score += 0.100
        score = min(score, 0.610)
        
        print("SCORE JA4 GERADO:", score)


        return score
    except:
        if old_ja4 != new_ja4:
            return 0.610
        return 0
    
    

def calculate_version_difference_score(old_version, new_version):
    try:
        # Converte as versões para listas de inteiros para comparação numérica
        old_version_parts = [int(part) for part in re.split(r'\D+', old_version) if part.isdigit()]
        new_version_parts = [int(part) for part in re.split(r'\D+', new_version) if part.isdigit()]
        
        # Compare cada parte da versão, da maior (major) para a menor (minor)
        for old, new in zip(old_version_parts, new_version_parts):
            if old != new:
                # Se houver diferença, calcule a pontuação com base na magnitude da mudança
                return 0.1 * (abs(old - new) / (max(old, new) + 0.1))
        
        # Se não houver diferença
        return 0
    except Exception as e:
        print(f"Error calculating version difference score: {e}")
        return 0

def classify_os(os_string):
    os_string = os_string.lower()
    if 'windows' in os_string:
        return 'Windows'
    elif 'linux' in os_string and 'android' not in os_string:
        return 'Linux'
    elif 'mac os' in os_string or 'macos' in os_string:
        return 'macOS'
    elif 'android' in os_string:
        return 'Android'
    elif 'ios' in os_string or 'iphone' in os_string or 'ipad' in os_string:
        return 'iOS'
    else:
        return 'Unknown'

def analyse_user_agent(old_ua, new_ua):
    try:
        score = 0
        
        # Extraia informações principais do User-Agent, como SO e versão
        old_os = re.search(r'\((.*?)\)', old_ua)
        new_os = re.search(r'\((.*?)\)', new_ua)
        
        old_os = old_os.group(1) if old_os else ""
        new_os = new_os.group(1) if new_os else ""
        
        # Classificar os SOs
        old_os_class = classify_os(old_ua)
        new_os_class = classify_os(new_ua)
        
        if old_os_class != new_os_class:
            # Mudança de categoria de SO - pontuação máxima
            return 10
        
        # Se não houve mudança de categoria, verifique as versões
        old_os_parts = old_os.split(";")
        new_os_parts = new_os.split(";")
        
        if len(old_os_parts) > 1 and len(new_os_parts) > 1:
            old_version = old_os_parts[1].strip()
            new_version = new_os_parts[1].strip()
            score += calculate_version_difference_score(old_version, new_version)
        
        # Limitar a pontuação a 1
        score = min(score, 10)
        
        return score
    except:
        if old_ua != new_ua:
            return 0.415
        return 0