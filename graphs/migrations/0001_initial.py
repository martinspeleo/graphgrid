# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'GraphGrid'
        db.create_table(u'graphs_graphgrid', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'graphs', ['GraphGrid'])

        # Adding model 'ObservationGraph'
        db.create_table(u'graphs_observationgraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('graph_grid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graphs.GraphGrid'])),
            ('row', self.gf('django.db.models.fields.IntegerField')()),
            ('column', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'graphs', ['ObservationGraph'])

        # Adding model 'ObservationGraphSeries'
        db.create_table(u'graphs_observationgraphseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('observation_graph', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graphs.ObservationGraph'])),
            ('observation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patients.NumericObservationType'])),
            ('colour', self.gf('colorful.fields.RGBColorField')(max_length=7)),
        ))
        db.send_create_signal(u'graphs', ['ObservationGraphSeries'])


    def backwards(self, orm):
        # Deleting model 'GraphGrid'
        db.delete_table(u'graphs_graphgrid')

        # Deleting model 'ObservationGraph'
        db.delete_table(u'graphs_observationgraph')

        # Deleting model 'ObservationGraphSeries'
        db.delete_table(u'graphs_observationgraphseries')


    models = {
        u'graphs.graphgrid': {
            'Meta': {'object_name': 'GraphGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'graphs.observationgraph': {
            'Meta': {'object_name': 'ObservationGraph'},
            'column': ('django.db.models.fields.IntegerField', [], {}),
            'graph_grid': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.GraphGrid']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'row': ('django.db.models.fields.IntegerField', [], {})
        },
        u'graphs.observationgraphseries': {
            'Meta': {'object_name': 'ObservationGraphSeries'},
            'colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.ObservationGraph']"}),
            'observation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.NumericObservationType']"})
        },
        u'patients.numericobservationtype': {
            'Meta': {'object_name': 'NumericObservationType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['graphs']