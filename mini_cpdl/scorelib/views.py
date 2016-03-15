import logging

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.generic.detail import DetailView

from .models import Score


logging.basicConfig(
    filename='views.log',
    filemode='w',
    level=logging.DEBUG,
    format='%(levelname)s:%(message)s'
)


def index(request):
    context = {'scores': []}
    if request.GET:
        logging.debug("request.GET: %s", request.GET)
        scores_queryset = Score.objects.all()
        if request.GET.get('voicing', None):
            logging.debug("voicing filter ran with voicing: %s", request.GET['voicing'])
            scores_queryset = scores_queryset.filter(
                voicing=request.GET.get('voicing', None)
            )
        if request.GET.get('composer', None):
            composer = request.GET['composer']
            logging.debug("composer filter ran with composer: %s", composer)
            scores_queryset = scores_queryset.filter(
                composer__icontains=composer
            )

        context['scores'] = scores_queryset

    return render_to_response('scorelib/index.html', context)


class ScoreDetailView(DetailView):
    pass
