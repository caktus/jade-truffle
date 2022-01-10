from django.shortcuts import render

from .models import ClientInternalLink

# Create your views here.
def list_links(request):
    links = ClientInternalLink.objects.all()
    return render(request, "client_onboarding/caktus_portal.html", {'links' : links}) 