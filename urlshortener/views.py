from django.shortcuts import render, redirect
from .models import ShortenedURL,Click
from .forms import UrlForm
from .shorten import Shortener
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from user_agents import parse

counter = 0

def shorten_url(request):
    global counter
    form = UrlForm(request.POST)
    token = ""

    if request.method == 'POST':
        if form.is_valid():
            long_url = form.cleaned_data['long_url']
            if is_valid_url(long_url):
                token = Shortener().generate_token()
                new_url = form.save(commit=False)
                new_url.short_url = token
                new_url.save()
                                                                           # Increment the counter for each new URL
                shortened_url_instance = ShortenedURL.objects.get(pk=1)
                shortened_url_instance.value = counter
                shortened_url_instance.save()
                counter += 1
            else:
                form.add_error('long_url', 'Enter a valid URL')
    else:
        form = UrlForm()
        token = "Invalid URL"

    return render(request, 'home.html', {'form': form, 'token': token, 'counter': counter})

def is_valid_url(url):
   validator = URLValidator()
   try:
        validator(url)
        return True
   except ValidationError:
        return False


def redirect_to_original_url(request, token):
    long_url = ShortenedURL.objects.filter(short_url=token)[0]
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    # Extract user platform and browser using a library like 'user-agents'
    user_agent_info = parse(user_agent)
    platform = user_agent_info.os.family
    browser = user_agent_info.browser.family

    # Record the click
    short_url = get_object_or_404(ShortenedURL, short_url=token)
    click = Click(short_url=short_url, user_agent=user_agent, platform=platform, browser=browser)
    click.save()
    return redirect(long_url.long_url)


def click_metrics(request, token):
    short_url = get_object_or_404(ShortenedURL, short_url=token)
    clicks = Click.objects.filter(short_url=short_url)
    context = {'short_url': short_url, 'clicks': clicks}
    return render(request, 'click_metrics.html', context)
