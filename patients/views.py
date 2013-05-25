from patients.forms import *
from django.shortcuts import render, redirect

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


