from django.db import models

# Create your models here.
class ClientInternalLink(models.Model):
    CATEGORIES = [
        ("GH", "GitHub"),
        ("BC", "Basecamp"),
        ("ZL", "Zeplin"),
        ("SL", "Slack"),
        ("OT", "Other"),
    ]
    name = models.CharField(max_length = 30)
    url = models.URLField()
    description = models.CharField(max_length=250)
    category = models.CharField(max_length=2, choices=CATEGORIES, default="OT")

    def image_url(self):
        if self.category == "GH":
            return "/static/images/github-logo.png"
        elif self.category == "BC":
            return "/static/images/basecamp-logo.png"
        elif self.category == "ZL":
            return "/static/images/zeplin-logo.png"
        elif self.category == "SL":
            return "/static/images/slack-logo.png"
        else:
            return "/static/images/caktus-logo-426x234.png"

    def get_color_value(self):
        if self.category == "GH":
            return "#1e75bb"
        elif self.category == "BC":
            return "#fde002"
        elif self.category == "ZL":
            return "#d9470e"
        elif self.category == "SL":
            return "#4d164e"
        else:
            return "#bbb"

    class Meta:
        verbose_name_plural = "Client Internal Links"