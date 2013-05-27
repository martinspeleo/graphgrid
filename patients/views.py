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
    import matplotlib.pyplot as plt

    start = datetime.datetime.strptime(start, "%Y-%m-%d-%H-%M")
    end = datetime.datetime.strptime(end, "%Y-%m-%d-%H-%M")
    min_ = float(min_)
    max_ = float(max_)
    refmin = float(refmin)
    refmax = float(refmax)     

    patient = get_object_or_404(Patient, mrn = mrn)

    fig=Figure(figsize=(float(width) / 80., float(height) / 80.))
    ax=fig.add_subplot(111)
    c = compass.lower()
    fig.subplots_adjust(left={True: 0.2, False:0}["w" in c], 
                        right={True: 0.9, False:1}["e" in c], 
                        bottom={True: 0.2, False:0}["s" in c], 
                        top={True: 0.9, False:1}["n" in c])
    #ax.set_frame_on(False)
    x=[]
    y=[]
    if obs == "bp":
        sbpt = get_object_or_404(NumericObservationType, name = "Systolic Blood Pressure")
        dbpt = get_object_or_404(NumericObservationType, name = "Diastolic Blood Pressure")
        sbp = NumericObservation.objects.filter(patient = patient, observation_type = sbpt)
        #dbp = NumericObservation.objects.filter(patient = patient, observation_type = dbpt)
        for s in sbp:#HACK||||||||
            try:
                d = NumericObservation.objects.get(patient = patient, observation_type = dbpt, datetime = s.datetime)
                ax.plot_date([s.datetime, d.datetime], [s.value, d.value], "b-")
            except:
                pass
        
    else:
        numericobservationtype = get_object_or_404(NumericObservationType, name = obs)
        nos = NumericObservation.objects.filter(patient = patient, observation_type = numericobservationtype)
        ax.plot_date([no.datetime for no in nos], [no.value for no in nos], '.')
    startday = datetime.date(start.year, start.month, start.day)
    for d in range(20):
            #try:HACK
                ax.plot_date([startday + datetime.timedelta(d), startday + datetime.timedelta(d)], [refmin, refmax], "y-")
            #except:
            #    pass
    ax.set_xlim( (start, end) )
    ax.set_ylim( (min_, max_) )
    ax.xaxis.set_ticks([start, end])
    ax.yaxis.set_ticks([min_, refmin, refmax, max_])
    ax.yaxis.set_ticks_position("both")
    rect = plt.Rectangle((start, refmin), end, refmax - refmin, facecolor="#dddddd", edgecolor="white")
    fig.gca().add_patch(rect)
    #ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #fig.autofmt_xdate()
    #fig.tight_layout(pad=0.5)
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response, )
    return response

