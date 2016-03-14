from django.http import HttpResponse
from django.shortcuts import render_to_response


def index(request):
    context = {'scores': Scores.objects.all()}
    return render_to_response('scorelib/index.html', context)
