# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'imageGraphSeries'
        db.create_table(u'graphs_imagegraphseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_graph', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graphs.imageGraph'])),
            ('colour', self.gf('colorful.fields.RGBColorField')(max_length=7)),
            ('observation_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patients.NumericObservationType'])),
            ('lower_value', self.gf('django.db.models.fields.FloatField')()),
            ('lower_pixel', self.gf('django.db.models.fields.FloatField')()),
            ('upper_value', self.gf('django.db.models.fields.FloatField')()),
            ('upper_pixel', self.gf('django.db.models.fields.FloatField')()),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('latest_value', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reference_lower', self.gf('django.db.models.fields.FloatField')()),
            ('reference_upper', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'graphs', ['imageGraphSeries'])

        # Adding model 'imageGraphSeriesLine'
        db.create_table(u'graphs_imagegraphseriesline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_graph_series', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graphs.imageGraphSeries'])),
            ('value', self.gf('django.db.models.fields.FloatField')()),
            ('othervalue', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('label', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linethickness', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'graphs', ['imageGraphSeriesLine'])

        # Adding model 'imageGraphTimeSeries'
        db.create_table(u'graphs_imagegraphtimeseries', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image_graph', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['graphs.imageGraph'])),
            ('time_period_days', self.gf('django.db.models.fields.FloatField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'graphs', ['imageGraphTimeSeries'])

        # Adding model 'imageGraph'
        db.create_table(u'graphs_imagegraph', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('height', self.gf('django.db.models.fields.IntegerField')()),
            ('width', self.gf('django.db.models.fields.IntegerField')()),
            ('left_border', self.gf('django.db.models.fields.FloatField')()),
            ('right_border', self.gf('django.db.models.fields.FloatField')()),
            ('central_axis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('now_axis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('linethickness', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'graphs', ['imageGraph'])


    def backwards(self, orm):
        # Deleting model 'imageGraphSeries'
        db.delete_table(u'graphs_imagegraphseries')

        # Deleting model 'imageGraphSeriesLine'
        db.delete_table(u'graphs_imagegraphseriesline')

        # Deleting model 'imageGraphTimeSeries'
        db.delete_table(u'graphs_imagegraphtimeseries')

        # Deleting model 'imageGraph'
        db.delete_table(u'graphs_imagegraph')


    models = {
        u'graphs.graphgrid': {
            'Meta': {'object_name': 'GraphGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'graphs.imagegraph': {
            'Meta': {'object_name': 'imageGraph'},
            'central_axis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_border': ('django.db.models.fields.FloatField', [], {}),
            'linethickness': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'now_axis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_border': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        },
        u'graphs.imagegraphseries': {
            'Meta': {'object_name': 'imageGraphSeries'},
            'colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraph']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'latest_value': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lower_pixel': ('django.db.models.fields.FloatField', [], {}),
            'lower_value': ('django.db.models.fields.FloatField', [], {}),
            'observation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.NumericObservationType']"}),
            'reference_lower': ('django.db.models.fields.FloatField', [], {}),
            'reference_upper': ('django.db.models.fields.FloatField', [], {}),
            'upper_pixel': ('django.db.models.fields.FloatField', [], {}),
            'upper_value': ('django.db.models.fields.FloatField', [], {})
        },
        u'graphs.imagegraphseriesline': {
            'Meta': {'object_name': 'imageGraphSeriesLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraphSeries']"}),
            'label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'linethickness': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'othervalue': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'graphs.imagegraphtimeseries': {
            'Meta': {'object_name': 'imageGraphTimeSeries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraph']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time_period_days': ('django.db.models.fields.FloatField', [], {})
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