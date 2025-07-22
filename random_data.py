import random
import uuid

def load_user_agents(file_path='user-agents.txt'):
    """Load user agents from a file into a list."""
    with open(file_path, 'r') as file:
        user_agents = [line.strip() for line in file.readlines()]
    return user_agents

def generate_random_json(user_agents):
    ja3_hash = str(uuid.uuid4()).replace('-', '')
    ja4_hash = "t13i" + str(random.randint(1000, 9999)) + "h1_" + ja3_hash[:12] + "_d" + ja3_hash[12:24]
    ja4h = "ge11cn" + str(random.randint(100000, 999999)) + "_" + ja3_hash[:12] + "_" + ja3_hash[12:24]
    ja4l = str(random.randint(1000, 9999)) + "_" + str(random.randint(10, 99)) + "_" + str(random.randint(10000, 99999))
    get_header_signature = str(uuid.uuid4()).replace('-', '')
    post_header_signature = str(uuid.uuid4()).replace('-', '')
    
    # Select a random user-agent from the provided list
    user_agent = random.choice(user_agents)
    
    content_length = str(random.randint(100, 1000))
    source_ipv4 = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}"
    
    return {
        "ja3_hash": ja3_hash,
        "ja4_hash": ja4_hash,
        "ja4h_hash": ja4h,
        "ja4l_hash": ja4l,
        "get_header_signature": get_header_signature,
        "post_header_signature": post_header_signature,
        "user_agent": user_agent,
        "content-length": content_length,
        "source_ipv4": source_ipv4
    }

# Load the user agents from the file
user_agents_list = load_user_agents()

# Generate a random JSON object using the loaded user agents
random_json = generate_random_json(user_agents_list)
print(random_json)
