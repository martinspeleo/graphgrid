from django.db import models
from colorful.fields import RGBColorField
from operator import itemgetter

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
