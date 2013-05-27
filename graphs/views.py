from django.shortcuts import render, get_object_or_404
from graphs.models import *
from patients.models import *
import datetime

dateformat = "%Y-%m-%d-%H-%M"

def home(request):
    graphgrids = GraphGrid.objects.all()
    return render(request, 'graphgrids.html', {'graphgrids': graphgrids})

def graphgrid(request, graphgrid):
    graphgrid = get_object_or_404(GraphGrid, name = graphgrid)
    return render(request, 'graphgrid.html', {'graphgrid': graphgrid})

def vitalsVis(request, mrn):
    patient = get_object_or_404(Patient, mrn = mrn)
    datetimenow = datetime.datetime(2010,11,01) 
    #datetimenow = datetime.datetime.now() 
    datetimeoneday = datetime.datetime.strftime(datetimenow - datetime.timedelta(1), dateformat)
    datetimefivedays = datetime.datetime.strftime(datetimenow - datetime.timedelta(5), dateformat)
    datetimezerodays = datetime.datetime.strftime(datetimenow, dateformat)
    datenow = datetime.datetime.strftime( datetimenow, "%d/%m/%Y")
    timenow = datetime.datetime.strftime( datetimenow, "%H:%M")
    try: 
        recentRR = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Respiratory Rate" ).order_by("-datetime")[0].value
    except:
        recentRR = "-"
	
    return render(request, 'vitalsvis.html', {'patient': patient, 'datenow': datenow, 'timenow': timenow, 'datetimeoneday': datetimeoneday, 'datetimefivedays': datetimefivedays, 'datetimezerodays': datetimezerodays, 'recentRR': recentRR, 'width': 300})
