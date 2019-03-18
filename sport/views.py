import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult, Compitition
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.template.context_processors import csrf


# Create your views here.

def index(request):
    return render(request, 'sport/competition.html')


def sport_view(request):
    sports = Sport.objects.all()
    context = {
        'sports': sports
    }
    return render(request, 'sport/competition.html', context)

'''
def table_view(request):
    team = Team.objects.all()
    period = Period.objects.all()
    place = Place.objects.all()
    sports = Sport.objects.all()

    context = {
        'sports': sports,
        'team': team,
        'period': period,
        'place': place
    }
    return render(request, 'sport/competition.html', context)
'''

def table_view(request):
    team = Team.objects.all()
    if 'period_id' in request.GET.keys():
        period = Period.objects.get(id=request.GET['period_id'])
    else:
        today = datetime.datetime.now()
        period = Period.objects.get(begin__lte=today, end__gte=today)
    sports = Sport.objects.all()
    results = TeamResult.objects.select_related('Team', 'Department', 'Compitition', 'Place').filter(compitition__date__gte=period.begin, compitition__date__lte=period.end)

    context = {
        'sports': sports,
        'period': period,
        'results':resultsr
    }
    return render(request, 'sport/competition.html', context)

def competition(request):
    competition = Compitition.objects.all()
    return render(request, 'sport/competitiond.html', locals())

def competitionedit(request, competition_id):
    args={'competition_id':competition_id}
    args.update(csrf(request))
    if request.POST:
        comment = request.POST.get('comment','')
        Compitition.objects.comment=comment
        #Compitition.objects.
        return redirect('/CM/competition/')
    else:
        return render(request, 'sport/competitiondEdit.html', args)
