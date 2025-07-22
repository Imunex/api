from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User

class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True
        ordering = ['created_at']
class User(TimeStamp):
    email = models.CharField(max_length=100)
    verified_count = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    last_device_failed_date = models.DateTimeField(null=True, blank=True)
    last_device_failed_ip_addr_v4 = models.CharField(max_length=50, null=True)
    last_device_failed_ip_addr_v6 = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)  # Chama o save original para salvar o objeto no BD

class Devices(TimeStamp):
    name = models.CharField(max_length=100, null=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="devices")
    verified = models.BooleanField(default=False)
    verified_date_created = models.DateTimeField(null=True, blank=True)
    verified_date_changed = models.DateTimeField(auto_now=True)
    verified_count = models.IntegerField(null=True)

    def __str__(self):
        return self.User.email
    
    def save(self, *args, **kwargs):
        User = self.User
        if User.devices.count() < 3:
            if not self.name:
                self.name = "Device "+str(User.devices.count()+1)
            super().save(*args, **kwargs)


class Scores(TimeStamp):
    device = models.ForeignKey(Devices, on_delete=models.CASCADE, related_name="scores")
    is_safe = models.BooleanField(default=False)
    score = models.FloatField()
    current_score_enhanced = models.FloatField(null = True)
    ja4 = models.CharField(max_length=100, null = True)
    ja4h = models.CharField(max_length=100, null = True)
    ja4l = models.CharField(max_length=100, null = True)
    ja3 = models.CharField(max_length=1000, null=True)
    get_header_signature = models.CharField(max_length=200, null=True)
    post_header_signature = models.CharField(max_length=200, null=True)
    content_length = models.CharField(max_length=50, null=True)
    source_ipv4 = models.CharField(max_length=50, null=True)
    user_agent = models.CharField(max_length=500)
    reason = models.CharField(max_length=500, null=True)
    source = models.CharField(max_length=100, null=True, default="API Call")
    
    def __str__(self):
        return self.device.User.email +" "+ str(self.created_at) if self.device else self.source_ipv4 +" "+ str(self.created_at)