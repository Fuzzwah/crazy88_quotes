from django.db import models

class Quote(models.Model):
    added_by_userid = models.CharField(max_length=255, null=True)
    added_by_username = models.CharField(max_length=255, null=True)
    teamid = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    channel = models.CharField(max_length=255)


class History(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    returned_at = models.DateTimeField(auto_now_add=True, blank=True)

