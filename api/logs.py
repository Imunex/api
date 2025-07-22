from datetime import datetime
from pytz import timezone
from api.utils import get_user_ip
from api.utils import set_data
from deviceprotect.settings import TIME_ZONE



class GenerateLogs():
    def __init__(self, request, severity, action ) -> None:
        self.logger = open('general.log', 'a')
        self.audit = open('audit.log', 'a')
        self.request = request
        ip = get_user_ip(request)
        self.severity = eval("self."+severity)
        method = request.method
        query_params = request.query_params

        if method == 'GET':
            data = {}
            data = set_data(data, request)
        else:
            data = request.data.copy()
            data= set_data(data, request)
            if email := data.get('email'):
                data['email'] = '****' + email[4:]
        now = datetime.now(tz=timezone(TIME_ZONE))
        now = now.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        api_key = request.headers.get('Authorization')
        try:
            api_key = api_key.split(' ')[1]
            self.logger.write(f"{now} area51.imunex.ai METHOD: {method} IP: '{ip}' ACTION: '{action}' ORGANIZATION: '{"Local Org"}' ")
            self.logger.write(f"{now} area51.imunex.ai DATA: {data} ")
        except Exception as e:
            print(e)
            self.logger.write(f"{now} area51.imunex.ai METHOD: {method} IP: '{ip}' ACTION: '{action}' ORGANIZATION: 'NOT FOUND' ")
        if query_params:
            self.logger.write(f"QUERY-PARAMS: {query_params} ")
        if data:
            if email := data.get('email'):
                email = '****' + email[4:]
                self.logger.write(f"EMAIL: {email} ")
        self.logger.write(f"{severity}: '")

    def INFO(self):
        self.logger.write(' SUCCESS')
    def ERROR(self):
        self.logger.write(' FAILED')
    def WARNING(self):
        ...
    def CRITICAL(self):
        ...

    def no_organization_error(self):
        self.logger.write("Organization is not active'")
        self.end_log()

    def suspicious_user_error(self,offensors=None):
        self.logger.write(f"Hash from suspicious source/device {offensors}")
        self.end_log()
    
    def end_log(self):
        self.logger.write("\n")
        self.logger.close()

    def write_log(self, message):
        self.logger.write(message+"'")
        self.severity()
        self.end_log()

    def audit_write(self, message):
        self.logger.write("USER:"+ self.request.user.username+" "+message+"'")
        self.severity()
        self.end_log()
