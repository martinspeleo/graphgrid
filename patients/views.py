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

