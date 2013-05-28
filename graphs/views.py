from django.shortcuts import render, get_object_or_404
from graphs.models import *
from patients.models import *
from graphs.ews import *
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
	#Calculate the date/time limits for day lines + graph separation
    datetimenow = datetime.datetime(2010,11,01) 
    #datetimenow = datetime.datetime.now() 
    datetimeoneday = datetime.datetime.strftime(datetimenow - datetime.timedelta(1), dateformat)
    datetimefivedays = datetime.datetime.strftime(datetimenow - datetime.timedelta(5), dateformat)
    datetimezerodays = datetime.datetime.strftime(datetimenow, dateformat)
    datenow = datetime.datetime.strftime( datetimenow, "%d/%m/%Y")
    timenow = datetime.datetime.strftime( datetimenow, "%H:%M")
	#Get most recent observations - if none, return "-"
    try: 
        recentRR = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Respiratory Rate" ).order_by("-datetime")[0].value
    except:
        recentRR = "-"
    try: 
        recentSpO2 = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Oxygen Saturation" ).order_by("-datetime")[0].value
    except:
        recentSpO2 = "-"
    try: 
        recentTemp = "%0.1f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Temperature" ).order_by("-datetime")[0].value
    except:
        recentTemp = "-"
    try: 
        recentSBP = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Systolic Blood Pressure" ).order_by("-datetime")[0].value
    except:
        recentSBP = "-"
    try: 
        recentDBP = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Diastolic Blood Pressure" ).order_by("-datetime")[0].value
    except:
        recentDBP = "-"
    try: 
        recentHR = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Heart Rate" ).order_by("-datetime")[0].value
    except:
        recentHR = "-"
	#calculate EWS
    try: 
        recentEWSCalc = calculateEWS( recentRR, recentSpO2, recentTemp, recentSBP, recentHR, 0, 0)
        recentEWS = recentEWSCalc['EWS']
    except:
        recentEWS = "-"
    #Return patient, date and observation details
    return render(request, 'vitalsvis.html', {'patient': patient, 'datenow': datenow, 'timenow': timenow, 'datetimeoneday': datetimeoneday, 'datetimefivedays': datetimefivedays, 'datetimezerodays': datetimezerodays, 'recentRR': recentRR, 'recentSpO2': recentSpO2, 'recentTemp': recentTemp, 'recentSBP': recentSBP, 'recentDBP': recentDBP, 'recentHR': recentHR, 'recentEWS': recentEWS, 'width': 290, 'height': 90, 'bpheight': 150})
