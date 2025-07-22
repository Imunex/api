# Copyright (c) 2023, FoxIO, LLC.
# All rights reserved.
# Patent Pending
# JA4H is licenced under the FoxIO License 1.1. For full license text, see the repo root.

# Copyright (c) 2023, FoxIO, LLC.
# All rights reserved.
# Patent Pending
# JA4 is Open-Source, Licensed under BSD 3-Clause
# JA4+ (JA4S, JA4H, JA4L, JA4X, JA4SSH) are licenced under the FoxIO License 1.1. For full license text, see the repo root.
#

from hashlib import sha256
from datetime import datetime
from typing import Dict

conn_cache = {}
quic_cache = {}
http_cache = {}
ssh_cache = {}

TLS_MAPPER = {'256': "s1",
              '512': "s2",
              '0x0300': "s3",
              '0x0301': "10",
              '0x0302': "11",
              '0x0303': "12",
              '0x0304': "13"}

GREASE_TABLE = {'0x0a0a': True, '0x1a1a': True, '0x2a2a': True, '0x3a3a': True,
                '0x4a4a': True, '0x5a5a': True, '0x6a6a': True, '0x7a7a': True,
                '0x8a8a': True, '0x9a9a': True, '0xaaaa': True, '0xbaba': True,
                '0xcaca': True, '0xdada': True, '0xeaea': True, '0xfafa': True}

def delete_keys(keys, x):
    for key in keys:
        if key in x:
            del(x[key])


######## SIMPLE CACHE FUNCTIONS #############################
# The idea is to record quic packets into a quic_cache
# and record tcp tls packets into a conn_cache
# The cache is indexed by the stream number and hold all the
# required data including timestamps
# we print final results from the cache

def get_cache(x):
    if x['hl'] in [ 'http', 'http2']:
        return http_cache
    elif x['hl'] == 'quic':
        return quic_cache
    else:
        return conn_cache

def clean_cache(x):
    cache = get_cache(x)
    if x['stream'] in cache:
        del(cache[x['stream']])

# Updates the cache and records timestamps
def cache_update(x, field, value, debug_stream=-1):
    cache = get_cache(x)
    stream = int(x['stream'])
    update = False

    if field == 'stream' and stream not in cache:
        cache[stream] = { 'stream': stream}
        return

    # Do not update main tuple fields if they are already in
    if field in [ 'stream', 'src', 'dst', 'srcport', 'dstport', 'A', 'B', 'JA4S', 'D', 'server_extensions', 'count', 'stats'] and field in cache[stream]:
        return

    # update protos only if we have extra information
    if field == 'protos':
        if field in cache[stream] and len(value) <= len(cache[stream][field]):
            return

    # special requirement for ja4c when the C timestamp needs to be the
    # the last before D
    if field == 'C' and 'D' in cache[stream]:
        return

    if stream in cache:
        if stream == debug_stream:
            print (f'updating ({"quic" if x["quic"] else "tcp"}) stream {stream} {field} {value}')
        cache[stream][field] = value
        update = True
    return update

###### END OF CACHE FUNCTIONS

# Joins an array by commas in the order they are presented
# and returns the first 12 chars of the sha256 hash
def sha_encode(values):
    if isinstance(values, list):
        return sha256(','.join(values).encode('utf8')).hexdigest()[:12]
    else:
        return sha256(values.encode('utf8')).hexdigest()[:12]

# processes ciphers found in a packet
# tshark keeps the ciphers either as a list or as a single value
# based on whether it is ciphersuites or ciphersuite
def get_hex_sorted(entry, field, sort=True):
    values = entry[field]
    if not isinstance(values, list):
        values = [ values ]

    # remove GREASE and calculate length
    c = [ x[2:] for x in values if x not in GREASE_TABLE ]
    actual_length = len(c)

    # now remove SNI and ALPN values
    if field == 'extensions' and sort:
        c = [ x for x in c if x not in ['0000', '0010']]

    c.sort() if sort else None

    return ','.join(c), '{:02d}'.format(actual_length), sha_encode(c)

def get_supported_version(v):
    if not isinstance(v, list):
        v = [ v ]
    versions = [ k for k in v if k not in GREASE_TABLE ]
    versions.sort()
    return versions[-1]


## Time diff of epoch times / 2
## computes t2 - t1
## returns diff in seconds
def epoch_diff(t1, t2):
    dt1 = datetime.fromtimestamp(float(t1))
    dt2 = datetime.fromtimestamp(float(t2))
    return int((dt2-dt1).microseconds/2)
    

# Scan for tls
def scan_tls(layer):
    if not layer:
        return None

    if not isinstance(layer, list):
        if 'tls_tls_handshake_type' in layer:
            return layer
    else:
        for l in layer:
            if 'tls_tls_handshake_type' in l:
                return l

# Get the right signature algorithms
def get_signature_algorithms(packet): 
    if 'sig_alg_lengths' in packet and isinstance(packet['sig_alg_lengths'], list):
        alg_lengths = [ int(int(x)/2) for x in packet['sig_alg_lengths'] ]

        extensions = packet['extensions']
        idx = 0
        try:
            if extensions.index('13') > extensions.index('35'):
                idx = 1 
        except Exception as e:
            pass
        packet['signature_algorithms'] = packet['signature_algorithms'][alg_lengths[idx]:]
    return [ x for x in packet['signature_algorithms'] if x not in GREASE_TABLE ]
        
######### HTTP FUNCTIONS ##############################
def http_method(method):
    return method.lower()[:2]

def http_language(lang):
    lang = lang.replace('-','').lower().split(',')[0]
    return f"{lang}{'0'*(4-len(lang))}"

def to_ja4h(x, debug_stream=-1):
    cookie = 'c' if 'cookies' in x else 'n'
    referer = 'r' if 'referer' in [ y.lower() for y in x['headers'] ] else 'n'
    method = http_method(x['method'])
    x['hl'] = 'https'
    version = 11 if x['hl'] == 'http' else 20
    unsorted_cookie_fields = []
    unsorted_cookie_values = []

    x['headers'] = [ h.split(':')[0] for h in x['headers'] ]
    x['headers'] = [ h for h in x['headers'] 
            if not h.startswith(':') and not h.lower().startswith('cookie') 
            and h.lower() != 'referer' and h ]

    raw_headers = x['headers'][:]

    #x['headers'] = [ '-'.join([ y.capitalize() for y in h.split('-')]) for h in x['headers'] ]
    header_len = '{:02d}'.format(len(x['headers']))
    try:
        if 'cookies' in x:
            if isinstance(x['cookies'], list):
                x['cookie_fields'] = [ y.split('=')[0] for y in x['cookies'] ]
                x['cookie_values'] = [ y.lstrip().rstrip() for y in x['cookies'] ]
            else:
                x['cookie_fields'] = [ y.split('=')[0] for y in x['cookies'].split(';') ]
                x['cookie_values'] = [ y.lstrip().rstrip() for y in x['cookies'].split(';') ]

            unsorted_cookie_fields = x['cookie_fields'][:]
            unsorted_cookie_values = x['cookie_values'][:]

            x['cookie_fields'].sort()
            x['cookie_values'].sort()

        cookies = sha_encode(x['cookie_fields']) if 'cookies' in x else '0'*12
        cookie_values = sha_encode(x['cookie_values']) if 'cookies' in x else '0'*12
    except:
        cookies = '0'*12
        cookie_values = '0'*12

    lang = http_language(x['lang']) if 'lang' in x and x['lang'] else '0000'
    headers = sha_encode(x['headers'])
    x['JA4H'] = f'{method}{version}{cookie}{referer}{header_len}{lang}_{headers}_{cookies if len(cookies) else ""}_{cookie_values}'
    x['JA4H_r'] = f"{method}{version}{cookie}{referer}{header_len}{lang}_{','.join(raw_headers)}_"
    x['JA4H_ro'] = f"{method}{version}{cookie}{referer}{header_len}{lang}_{','.join(raw_headers)}_"
    if 'cookie_fields' in x:
        x['JA4H_ro'] += f"{','.join(unsorted_cookie_fields)}_{','.join(unsorted_cookie_values)}"
        x['JA4H_r'] += f"{','.join(x['cookie_fields'])}_{','.join(x['cookie_values'])}"
    # cache_update(x, 'JA4H', x['JA4H'], debug_stream)
    # cache_update(x, 'JA4H_r', x['JA4H_r'], debug_stream)
    # cache_update(x, 'JA4H_ro', x['JA4H_ro'], debug_stream)
    return x

############# END OF HTTP FUNCTIONS ##################

def get_ja4h(request: Dict[str, str]) -> str:
    x = {
        'method': request.method,
        'headers': request.headers,  # Example: replace 'YOUR_HEADER_NAME'
        'cookies': request.headers.get("Cookie"),  # Example: replace 'your_cookie_name'
        'referer': request.headers.get('referer'),
        'lang': request.headers.get('Accept-Language')
        # Add other relevant details
    }

    # Call the to_ja4h function to generate the JA4H hash
    x = to_ja4h(x)
    return x['JA4H']