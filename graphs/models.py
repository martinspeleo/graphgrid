from django.db import models
from colorful.fields import RGBColorField

class GraphGrid(models.Model):
    name = models.CharField(max_length=200)

    def __unicode___(self):
        return self.name

class ObservationGraph(models.Model):
    graph_grid =  models.ForeignKey("GraphGrid")
    row =  models.IntegerField()
    column = models.IntegerField()

    def __unicode___(self):
        return "%s(%i, %i)" % (self.name, self.row, self.column)

class ObservationGraphSeries(models.Model):
    observation_graph =  models.ForeignKey("ObservationGraph")
    observation_type =  models.ForeignKey("patients.NumericObservationType")
    colour = RGBColorField()

    def __unicode___(self):
        return "%s: %s" % (self.observation_graph, self.observation_type)
