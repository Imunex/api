from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTWebsocketMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_params = dict(
            param.split("=") 
            for param in scope["query_string"].decode().split("&") 
            if "=" in param
        )
        
        from asgiref.sync import sync_to_async

        token = query_params.get("token")
        if token:
            try:
                auth = JWTAuthentication()
                validated_token = await sync_to_async(auth.get_validated_token)(token)
                user = await sync_to_async(auth.get_user)(validated_token)
                scope["user"] = user
            except Exception as er:
                scope["user"] = AnonymousUser()
        else:
            scope["user"] = AnonymousUser()
        return await self.app(scope, receive, send)