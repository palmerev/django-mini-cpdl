from django.http import HttpResponse
from django.shortcuts import render_to_response

from .models import Score


def index(request):
    context = {'scores': Score.objects.filter(
        voicing=request.GET.get('voicing', None)
    )}
    return render_to_response('scorelib/index.html', context)
