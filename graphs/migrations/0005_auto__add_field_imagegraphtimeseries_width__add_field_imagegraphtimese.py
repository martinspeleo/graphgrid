# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'imageGraphTimeSeries.width'
        db.add_column(u'graphs_imagegraphtimeseries', 'width',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'imageGraphTimeSeries.major_tick_spacing'
        db.add_column(u'graphs_imagegraphtimeseries', 'major_tick_spacing',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'imageGraphTimeSeries.minor_tick_spacing'
        db.add_column(u'graphs_imagegraphtimeseries', 'minor_tick_spacing',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'imageGraph.top_border'
        db.add_column(u'graphs_imagegraph', 'top_border',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'imageGraph.bottom_border'
        db.add_column(u'graphs_imagegraph', 'bottom_border',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'imageGraphTimeSeries.width'
        db.delete_column(u'graphs_imagegraphtimeseries', 'width')

        # Deleting field 'imageGraphTimeSeries.major_tick_spacing'
        db.delete_column(u'graphs_imagegraphtimeseries', 'major_tick_spacing')

        # Deleting field 'imageGraphTimeSeries.minor_tick_spacing'
        db.delete_column(u'graphs_imagegraphtimeseries', 'minor_tick_spacing')

        # Deleting field 'imageGraph.top_border'
        db.delete_column(u'graphs_imagegraph', 'top_border')

        # Deleting field 'imageGraph.bottom_border'
        db.delete_column(u'graphs_imagegraph', 'bottom_border')


    models = {
        u'graphs.graphgrid': {
            'Meta': {'object_name': 'GraphGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'graphs.imagegraph': {
            'Meta': {'object_name': 'imageGraph'},
            'bottom_border': ('django.db.models.fields.FloatField', [], {}),
            'central_axis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'left_border': ('django.db.models.fields.FloatField', [], {}),
            'linethickness': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'now_axis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'right_border': ('django.db.models.fields.FloatField', [], {}),
            'top_border': ('django.db.models.fields.FloatField', [], {}),
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
            'upper_pixel': ('django.db.models.fields.FloatField', [], {}),
            'upper_value': ('django.db.models.fields.FloatField', [], {})
        },
        u'graphs.imagegraphseriesline': {
            'Meta': {'object_name': 'imageGraphSeriesLine'},
            'colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
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
            'major_tick_spacing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'minor_tick_spacing': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'time_period_days': ('django.db.models.fields.FloatField', [], {}),
            'width': ('django.db.models.fields.FloatField', [], {})
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