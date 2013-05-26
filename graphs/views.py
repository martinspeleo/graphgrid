from django.shortcuts import render, get_object_or_404
from graphs.models import *
from patients.models import *
import datetime

def home(request):
    graphgrids = GraphGrid.objects.all()
    return render(request, 'graphgrids.html', {'graphgrids': graphgrids})

def graphgrid(request, graphgrid):
    graphgrid = get_object_or_404(GraphGrid, name = graphgrid)
    return render(request, 'graphgrid.html', {'graphgrid': graphgrid})
def vitalsVis(request, mrn):
    patient = get_object_or_404(Patient, mrn = mrn)
    datetimeonedaytemp = datetime.datetime.now() - datetime.timedelta(1)
    datetimeoneday = datetime.datetime.strftime(datetimeonedaytemp, "%Y-%m-%d-%H-%M")
    datetimefivedaystemp = datetime.datetime.now() - datetime.timedelta(5) 
    datetimefivedays = datetime.datetime.strftime(datetimefivedaystemp, "%Y-%m-%d-%H-%M")
    return render(request, 'vitalsvis.html', {'patient': patient, 'datetimenow': datetime.datetime.now(), 'datetimeoneday': datetimeoneday, 'datetimefivedays': datetimefivedays})
