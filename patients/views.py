from patients.forms import *
from patients.models import *

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import json

def registerPatient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
        
    else:
        form = PatientForm()
    return render(request, "register_patient.html", {
        "form": form,
    })

def patientObservation(request):
    if request.method == 'POST':
        form = NumericObservationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = NumericObservationForm()
    return render(request, "numeric_observation.html", {
        "form": form,
    })

def getObs(request, mrn, obs):
    patient = get_object_or_404(Patient, mrn = mrn)
    numericobservationtype = get_object_or_404(NumericObservationType, name = obs)
    obs = NumericObservation.objects.filter(patient = patient, observation_type = numericobservationtype)
    response = HttpResponse()#content_type='text/json')    
    response.write(json.dumps([(o.datetime.isoformat(), o.value) for o in obs]))
    return response

def g(request, mrn, obs, start, end, compass, height, width, min_, max_, refmin, refmax):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    patient = get_object_or_404(Patient, mrn = mrn)
    numericobservationtype = get_object_or_404(NumericObservationType, name = obs)

    fig=Figure(figsize=(float(height) / 80., float(width) / 80.))
    ax=fig.add_subplot(111)
    c = compass.lower()
    fig.subplots_adjust(left={True: 0.2, False:0}["w" in c], 
                        right={True: 0.9, False:1}["e" in c], 
                        bottom={True: 0.1, False:0}["s" in c], 
                        top={True: 0.9, False:1}["n" in c])
    #ax.set_frame_on(False)
    x=[]
    y=[]
    nos = NumericObservation.objects.filter(patient = patient, observation_type = numericobservationtype)
    ax.plot_date([no.datetime for no in nos], [no.value for no in nos], '-')
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #fig.autofmt_xdate()
    #fig.tight_layout(pad=0.5)
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response, )
    return response

