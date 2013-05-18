from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    dob = models.DateField("date of birth")
    mrn = models.CharField("medical_record_number", max_length=20, unique = True)

    def __unicode___(self):
        return self.mrn

class NumericObservationType(models.Model):
    name = models.CharField(max_length=200, unique = True)
    units = models.CharField(max_length=200)

    def __unicode___(self):
        return self.name

class NumericObservation(models.Model):
    patient = models.ForeignKey("Patient")
    observation_type = models.ForeignKey("NumericObservationType")
    value = models.FloatField()

    def __unicode___(self):
        return u"%s: %s: %f" % (self.patient, self.observation_type, self.value)
