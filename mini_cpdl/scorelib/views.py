from django.http import HttpResponse
from django.shortcuts import render_to_response

from .models import Score


def index(request):
    context = {'scores': Score.objects.all()}
    return render_to_response('scorelib/index.html', context)
