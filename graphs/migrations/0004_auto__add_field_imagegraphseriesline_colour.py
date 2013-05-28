# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'imageGraphSeriesLine.colour'
        db.add_column(u'graphs_imagegraphseriesline', 'colour',
                      self.gf('colorful.fields.RGBColorField')(default='#000000', max_length=7),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'imageGraphSeriesLine.colour'
        db.delete_column(u'graphs_imagegraphseriesline', 'colour')


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