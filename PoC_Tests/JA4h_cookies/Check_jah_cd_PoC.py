import hashlib
import sys

# Custom hash from ja4h including the comma
def custom_sha256_encode(value):
    return hashlib.sha256("".join(value).encode('utf8')).hexdigest()[:12]

# Check if an argument is provided
if len(sys.argv) > 1:
    input_string = sys.argv[1]
    print("Custom hash ja4h_cd:", custom_sha256_encode(input_string))
else:
    print("No input string provided")



