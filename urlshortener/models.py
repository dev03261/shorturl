from django.db import models

class ShortenedURL(models.Model):
    short_url = models.CharField(max_length=20)
    long_url = models.URLField(default='https://example.com')
    value = models.IntegerField(default=0)






class Click(models.Model):
    short_url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE)
    user_agent = models.CharField(max_length=255)  # User agent string
    platform = models.CharField(max_length=255)    # User's platform (e.g., Windows, macOS)
    browser = models.CharField(max_length=255)     # User's browser (e.g., Chrome, Firefox)
    timestamp = models.DateTimeField(auto_now_add=True)
