from django.shortcuts import render, get_object_or_404
from patients.models import Patient, NumericObservation
from graphs.models import GraphGrid, imageGraph
from django.http import HttpResponse
from graphs.ews import *
import datetime
from PIL import Image, ImageDraw


dateformat = "%Y-%m-%d-%H-%M"

def home(request):
    graphgrids = GraphGrid.objects.all()
    return render(request, 'graphgrids.html', {'graphgrids': graphgrids})

def graphgrid(request, graphgrid):
    graphgrid = get_object_or_404(GraphGrid, name = graphgrid)
    return render(request, 'graphgrid.html', {'graphgrid': graphgrid})

def image_graph(request, mrn, graph_name):
    datetimenow = datetime.datetime(2010,11,01)
    patient = get_object_or_404(Patient, mrn = mrn)
    imagegraph = get_object_or_404(imageGraph, name = graph_name)
    i = Image.new("RGB", (imagegraph.width, imagegraph.height), "white")
    draw = ImageDraw.Draw(i)
    #Right Border
    lb = imagegraph.left_border
    rb = imagegraph.width - imagegraph.right_border
    tb = imagegraph.top_border
    bb = imagegraph.height - imagegraph.bottom_border
    time_series = imagegraph.imagegraphtimeseries_set.all()
    graph_series = imagegraph.imagegraphseries_set.all()
    for ls in graph_series:
        for l in ls.imagegraphseriesline_set.all():
            pixel = ls.get_pos(l.value)
            if l.linethickness:
                draw.line((lb, pixel, rb, pixel), 
                       width = int(imagegraph.linethickness),
                       fill = l.line_colour)
            if l.othervalue:
                otherpixel = ls.get_pos(l.othervalue) 
                draw.rectangle((lb, pixel, rb, otherpixel), 
                       fill = l.line_colour)
    if imagegraph.now_axis:
         draw.line((rb, tb, rb, bb), 
              width = int(imagegraph.linethickness),
              fill = "black")
    startdatetime = datetimenow
    tlb = rb
    for ts in time_series:
        enddatetime = startdatetime
        startdatetime = enddatetime - datetime.timedelta(ts.time_period_days)
        trb = tlb
        tlb = tlb - ts.width
        if ts.left_axis:
            draw.line((tlb, tb, tlb, bb), 
                       width = int(imagegraph.linethickness),
                       fill = "black")
            for ls in graph_series:
                for l in ls.imagegraphseriesline_set.all():
                    if l.label:
                        options = {}
                        drawTickLabel(draw, 
                                      "%s %s" % (str(l.value), 
                                                 ls.observation_type.units), 
                                      tlb, 
                                      ls.get_pos(l.value), 
                                      l.label_colour, 
                                      **options)
                        if l.othervalue:
                            drawTickLabel(draw, 
                                          "%s %s" % (str(l.othervalue), 
                                                     ls.observation_type.units), 
                                          tlb, 
                                          ls.get_pos(l.othervalue), 
                                          l.label_colour, 
                                          **options)
        for ls in graph_series:
            print startdatetime, enddatetime
            for n in NumericObservation.objects.filter(patient = patient, 
                                                       observation_type = ls.observation_type, 
                                                       datetime__lt = enddatetime, 
                                                       datetime__gt = startdatetime
                                                       ):
                t = trb - ts.get_pixels(enddatetime - n.datetime.replace(tzinfo=None))
                y = ls.get_pos(n.value)
                draw.ellipse((t - 1, y - 1, t + 1, y + 1), ls.line_colour)
    del draw
    response=HttpResponse(content_type='image/png')
    i.save(response, "PNG")
    return response

def drawTickLabel(draw, string, x, y, colour, **options):
                        sizeX, sizeY = draw.textsize(string, **options)
                        x = x - sizeX / 2 
                        y = y - sizeY / 2
                        #draw.rectangle((x - 1, y - 1, x + sizeX, y + sizeY), fill = "white")
                        draw.text((x, y), string, fill=colour, **options)

def vitalsVis(request, mrn):
    patient = get_object_or_404(Patient, mrn = mrn)
	#Calculate the date/time limits for day lines + graph separation
    datetimenow = datetime.datetime(2010,11,01) 
    #datetimenow = datetime.datetime.now() 
    datetimeoneday = datetime.datetime.strftime(datetimenow - datetime.timedelta(1), dateformat)
    datetimefivedays = datetime.datetime.strftime(datetimenow - datetime.timedelta(5), dateformat)
    datetimezerodays = datetime.datetime.strftime(datetimenow, dateformat)
    datenow = datetime.datetime.strftime( datetimenow, "%d/%m/%Y")
    timenow = datetime.datetime.strftime( datetimenow, "%H:%M")
	#Get most recent observations - if none, return "-"
    try: 
        recentRR = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Respiratory Rate" ).order_by("-datetime")[0].value
    except:
        recentRR = "-"
    try: 
        recentSpO2 = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Oxygen Saturation" ).order_by("-datetime")[0].value
    except:
        recentSpO2 = "-"
    try: 
        recentTemp = "%0.1f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Temperature" ).order_by("-datetime")[0].value
    except:
        recentTemp = "-"
    try: 
        recentSBP = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Systolic Blood Pressure" ).order_by("-datetime")[0].value
    except:
        recentSBP = "-"
    try: 
        recentDBP = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Diastolic Blood Pressure" ).order_by("-datetime")[0].value
    except:
        recentDBP = "-"
    try: 
        recentHR = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Heart Rate" ).order_by("-datetime")[0].value
    except:
        recentHR = "-"
	#calculate EWS
    try: 
        recentEWSCalc = calculateEWS( recentRR, recentSpO2, recentTemp, recentSBP, recentHR, 0, 0)
        recentEWS = recentEWSCalc['EWS']
    except:
        recentEWS = "-"
    #Return patient, date and observation details
    return render(request, 'vitalsvis.html', {'patient': patient, 'datenow': datenow, 'timenow': timenow, 'datetimeoneday': datetimeoneday, 'datetimefivedays': datetimefivedays, 'datetimezerodays': datetimezerodays, 'recentRR': recentRR, 'recentSpO2': recentSpO2, 'recentTemp': recentTemp, 'recentSBP': recentSBP, 'recentDBP': recentDBP, 'recentHR': recentHR, 'recentEWS': recentEWS, 'width': 290, 'height': 90, 'bpheight': 150})
