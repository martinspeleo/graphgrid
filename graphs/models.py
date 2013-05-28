from django.db import models
from colorful.fields import RGBColorField
from operator import itemgetter
import datetime

class GraphGrid(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    def grapharray(self):
        print dir(self)
        d = {}
        for g in self.observationgraph_set.all():
            if not d.has_key(g.row):
                d[g.row] = []
            d[g.row].append(g)
        return [sortbycol(graphs) for (row, graphs) in sorted(d.items(), key=itemgetter(0))]

def sortbycol(graphs):
    return sorted(graphs, key=lambda g: g.column)
    

class ObservationGraph(models.Model):
    graph_grid =  models.ForeignKey("GraphGrid")
    row =  models.IntegerField()
    column = models.IntegerField()

    def __unicode__(self):
        return "%s(%i, %i)" % (self.graph_grid, self.row, self.column)

class ObservationGraphSeries(models.Model):
    class Meta: 
        verbose_name_plural = "Observation Graph Series"
    observation_graph =  models.ForeignKey("ObservationGraph")
    observation_type =  models.ForeignKey("patients.NumericObservationType")
    colour = RGBColorField()
    def __unicode__(self):
        return "%s: %s" % (self.observation_graph, self.observation_type)

class imageGraph(models.Model):
    name = models.CharField(max_length=200)
    height = models.IntegerField()
    width = models.IntegerField()
    left_border = models.FloatField()
    right_border = models.FloatField()
    top_border = models.FloatField()
    bottom_border = models.FloatField()
    now_axis = models.BooleanField()
    linethickness = models.FloatField()

class imageGraphTimeSeries(models.Model):
    image_graph = models.ForeignKey("imageGraph")
    time_period_days = models.FloatField()
    width = models.FloatField()
    major_tick_spacing = models.FloatField(null = True, blank = True)
    minor_tick_spacing = models.FloatField(null = True, blank = True)
    order = models.IntegerField()
    left_axis = models.BooleanField()
    #class Meta: 
    #    orderby = "order"
    def get_pixels(self, dt):
        return self.width * (self.time_period_days - dt.total_seconds() / 86400. ) / self.time_period_days

class imageGraphSeries(models.Model):
    image_graph = models.ForeignKey("imageGraph")
    label_colour = RGBColorField()
    line_colour = RGBColorField()
    observation_type = models.ForeignKey("patients.NumericObservationType")
    lower_value = models.FloatField()
    lower_pixel = models.FloatField()
    upper_value = models.FloatField()
    upper_pixel = models.FloatField()
    label = models.CharField(max_length=200)
    latest_value = models.BooleanField()
    
    def get_pos(self, v):
        return self.lower_pixel + (self.upper_pixel - self.lower_pixel) * (v - self.lower_value) / (self.upper_value - self.lower_value)

class imageGraphSeriesLine(models.Model):
    image_graph_series = models.ForeignKey("imageGraphSeries")
    value = models.FloatField()
    othervalue = models.FloatField(null = True, blank = True)
    label = models.BooleanField()
    linethickness = models.FloatField(null = True, blank = True)
    label_colour = RGBColorField()
    line_colour = RGBColorField()
    
    
