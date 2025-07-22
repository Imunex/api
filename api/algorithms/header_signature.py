import hashlib

def header_signature(request):
    """
    This function returns the header signature
    """
    values = {
        "accept": "1",
        "accept-encoding": "2",
        "accept-language": "3",
        "connection": "4",
        "host": "5",
        "user-agent": "6",
        "cookie": "7",
        "content-length": "8",
        "content-type": "9"
    }

    order = list(request.headers.keys())
    ordering_values = [values.get(x.lower(), "0") for x in order]
    final_order = None
    for i in ordering_values:
        final_order = final_order + i if final_order else i
    enconded_order = final_order.encode('utf-8')
    hashed_order = hashlib.sha256(enconded_order).hexdigest()
    return hashed_order
