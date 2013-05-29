# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'imageGraphSeries.lower_pixel'
        db.delete_column(u'graphs_imagegraphseries', 'lower_pixel')

        # Deleting field 'imageGraphSeries.upper_pixel'
        db.delete_column(u'graphs_imagegraphseries', 'upper_pixel')

        # Adding field 'imageGraphSeries.pixel_height'
        db.add_column(u'graphs_imagegraphseries', 'pixel_height',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'imageGraphSeries.order'
        db.add_column(u'graphs_imagegraphseries', 'order',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'imageGraphSeries.decimal_places'
        db.add_column(u'graphs_imagegraphseries', 'decimal_places',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'imageGraphSeries.lower_pixel'
        db.add_column(u'graphs_imagegraphseries', 'lower_pixel',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Adding field 'imageGraphSeries.upper_pixel'
        db.add_column(u'graphs_imagegraphseries', 'upper_pixel',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)

        # Deleting field 'imageGraphSeries.pixel_height'
        db.delete_column(u'graphs_imagegraphseries', 'pixel_height')

        # Deleting field 'imageGraphSeries.order'
        db.delete_column(u'graphs_imagegraphseries', 'order')

        # Deleting field 'imageGraphSeries.decimal_places'
        db.delete_column(u'graphs_imagegraphseries', 'decimal_places')


    models = {
        u'graphs.graphgrid': {
            'Meta': {'object_name': 'GraphGrid'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'graphs.imagegraph': {
            'Meta': {'object_name': 'imageGraph'},
            'bottom_border': ('django.db.models.fields.FloatField', [], {}),
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
            'Meta': {'ordering': "['order']", 'object_name': 'imageGraphSeries'},
            'decimal_places': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraph']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'label_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'latest_value': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'line_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'lower_value': ('django.db.models.fields.FloatField', [], {}),
            'observation_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patients.NumericObservationType']"}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'other_observation_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'imagegraphseriesother'", 'null': 'True', 'to': u"orm['patients.NumericObservationType']"}),
            'pixel_height': ('django.db.models.fields.FloatField', [], {}),
            'upper_value': ('django.db.models.fields.FloatField', [], {})
        },
        u'graphs.imagegraphseriesline': {
            'Meta': {'object_name': 'imageGraphSeriesLine'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph_series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraphSeries']"}),
            'label': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'label_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'line_colour': ('colorful.fields.RGBColorField', [], {'max_length': '7'}),
            'linethickness': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'othervalue': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'graphs.imagegraphtimeseries': {
            'Meta': {'ordering': "['order']", 'object_name': 'imageGraphTimeSeries'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_graph': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['graphs.imageGraph']"}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'left_axis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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