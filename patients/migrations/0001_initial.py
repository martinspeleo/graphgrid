# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Patient'
        db.create_table(u'patients_patient', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('dob', self.gf('django.db.models.fields.DateField')()),
            ('mrn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal(u'patients', ['Patient'])

        # Adding model 'NumericObservationType'
        db.create_table(u'patients_numericobservationtype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('units', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'patients', ['NumericObservationType'])

        # Adding model 'NumericObservation'
        db.create_table(u'patients_numericobservation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('patient', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patients.Patient'])),
            ('observation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patients.NumericObservationType'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'patients', ['NumericObservation'])


    def backwards(self, orm):
        # Deleting model 'Patient'
        db.delete_table(u'patients_patient')

        # Deleting model 'NumericObservationType'
        db.delete_table(u'patients_numericobservationtype')

        # Deleting model 'NumericObservation'
        db.delete_table(u'patients_numericobservation')


    models = {
        u'patients.numericobservation': {
            'Meta': {'object_name': 'NumericObservation'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.NumericObservationType']"}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.Patient']"}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'patients.numericobservationtype': {
            'Meta': {'object_name': 'NumericObservationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'patients.patient': {
            'Meta': {'object_name': 'Patient'},
            'dob': ('django.db.models.fields.DateField', [], {}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'mrn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['patients']