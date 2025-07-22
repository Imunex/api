from datetime import datetime
from pytz import timezone
from typing import Dict, Tuple

from api.models.models import User
from api.algorithms.ja4h import get_ja4h
from api.algorithms.header_signature import header_signature

from deviceprotect.settings import TIME_ZONE
import hashlib

def get_user_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR', 'unknown')
    return ip

def fail_occurred(data):
    """
    This function checks if the failed occurred
    """
    user = User.objects.get(email=data.get('email'))
    user.last_device_failed_date = datetime.now(tz=timezone(TIME_ZONE))
    user.last_device_failed_ip_addr_v4 = data.get('source_ipv4')
    user.save()

def is_account_new(data: Dict[str, str]) -> Tuple[bool, User | None]:
    """
    This function checks if the account is new or not
    """
    email = data.get('email')
    user = User.objects.prefetch_related('devices').filter(email=email)
    if user.exists():
        return False, user.first()
    return True, None

def set_data(data: dict, request, get = False):
    """
    This function sets the data
    """
    data['user_agent'] = request.META.get('HTTP_USER_AGENT', 'unknown')
    data['source_ipv4'] = get_user_ip(request)
    print(request.headers) 

    
    data['ja4_string'] =request.headers.get('ja4-string')

    ja3 = request.headers.get('x_imunex_ja3', None)
    print("debug: At ", datetime.now(), " x_imunex_ja3: ", ja3)
    print("debug: At ", datetime.now(), " cloudfront-ja3: ", request.headers.get('cloudfront-viewer-ja3-fingerprint', None))
    if not ja3:
        ja3 = request.headers.get('cloudfront-viewer-ja3-fingerprint')
        if not ja3  :
            ja3=request.headers.get('cf-ja3-hash',None)
        print("debug: At ", datetime.now(), " cf-ja3-hash: ", ja3)
    if ja3:
        data['ja3'] = ja3
    else:
        ja3=request.headers.get('Ja3',None)
        print("debug: At ", datetime.now(), " Ja3: ", ja3) 
        data['ja3'] = hashlib.md5(ja3.encode()).hexdigest() if ja3 else None
    
    ja4= request.headers.get('x_imunex_ja4', None)
    print("debug: At ", datetime.now(), " x_imunex_ja4: ", request.headers.get('x_imunex_ja4',None))
    if not ja4:
        ja4 = request.headers.get('cloudfront-viewer-ja4-fingerprint')
        print("debug: At ", datetime.now(), "cloudfront-viewer-ja4-fingerprint: ", ja4)
        if not ja4  :
            ja4=request.headers.get('cf-ja4-hash',None)
            print("debug: At ", datetime.now(), " cf-ja4-hash: ", ja4)
    if ja4:
        data['ja4'] = ja4
    else:
        ja4=request.headers.get('Ja4',None)
        print("debug: At ", datetime.now(), " Ja4: ", ja4) 
        data['ja4'] = ja4


    data['ja4h'] = get_ja4h(request)
    data['content_length'] = request.headers.get('Content-Length')
    if get:
        data['get_header_signature'] = header_signature(request)
    else:
        data['post_header_signature'] = header_signature(request)
    return data
