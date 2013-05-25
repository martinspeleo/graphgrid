from django.forms import ModelForm
from patients.models import *

# Create the form class.
class PatientForm(ModelForm):
    class Meta:
        model = Patient

class NumericObservationForm(ModelForm):
    class Meta:
        model = NumericObservation
