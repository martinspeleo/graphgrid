from django.contrib import admin
from models import *

admin.site.register(GraphGrid)
admin.site.register(ObservationGraph)
admin.site.register(ObservationGraphSeries)

class imageGraphTimeSeriesInline(admin.TabularInline):
    model = imageGraphTimeSeries
    fk_name = "image_graph"

class imageGraphSeriesInline(admin.TabularInline):
    model = imageGraphSeries
    fk_name = "image_graph"

class imageGraphSeriesLineInline(admin.TabularInline):
    model = imageGraphSeriesLine
    fk_name = "image_graph_series"

class imageGraphAdmin(admin.ModelAdmin):
    inlines = [
        imageGraphTimeSeriesInline,
        imageGraphSeriesInline
    ]

class imageGraphSeriesAdmin(admin.ModelAdmin):
    inlines = [
        imageGraphSeriesLineInline
    ]

admin.site.register(imageGraph, imageGraphAdmin)
admin.site.register(imageGraphSeries, imageGraphSeriesAdmin)
