import datetime

from django.template.context_processors import csrf
from django.db.models import Q
from django.contrib import auth
from django.shortcuts import render, redirect
from django.http import HttpResponse
from sport.models import Sport, Period, Team, Place, TeamResult, Compitition, Judge, Person, CompetitionJudge
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.template.context_processors import csrf
from .forms import CompetitionForm, JudgeForm


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
    if 'q' in request.GET.keys():
        args={}
        query = request.GET.get('q')
        founded_values = Compitition.objects.filter(
            Q(sport__name__icontains = query)|
            Q(place__name__icontains = query)
        )
        args['competition'] = founded_values
        args['search_values'] = 'Результаты поиска: ' + str(founded_values.count()) + ' результатов по запросу "' + str(query) + '"'
        return render(request, 'sport/competitiond.html', args)
    return render(request, 'sport/competitiond.html', locals())

def competitionedit(request, competition_id):
    competition = Compitition.objects.get(pk = competition_id)
    judge = CompetitionJudge.objects.filter(compitition__id = competition_id).first()
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=competition)
        form1 = JudgeForm(request.POST, instance = judge)
        print(form1)
        args={}
        if request.POST['button']=='save':
            if form.is_valid():
                try:
                    form.save()
                    form1.instance.compitition = form.instance
                    if form1.is_valid():
                        form1.save()
                except Exception as e:
                    args['save_error']=str(e)
                    return  render(request, 'sport/competitiondEdit.html', args)
            return redirect("sport:competition")
        if request.POST['button']=='delete':
            Compitition.objects.filter(id=competition_id).delete()
            return redirect("sport:competition")
        if request.POST['button']=='copy':
            return render(request, 'sport/competitiondEdit.html', {
                'form': CompetitionForm(instance=competition),
                'form1': JudgeForm(instance = judge)
                })
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(instance = competition),
        'form1': JudgeForm(instance = judge)
        })

def competitioncreate(request):
    args={}
    args['create'] = 'true'
    if request.method == 'POST':
        form = CompetitionForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                args['save_error']=str(e)
                return  render(request, 'sport/competitiondEdit.html', args)
        return redirect("sport:competition")
    return render(request, 'sport/competitiondEdit.html', {
        'form': CompetitionForm(),
        'form1': JudgeForm(),
        'create': 'create'
        })
