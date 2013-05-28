from django.shortcuts import render, get_object_or_404
from patients.models import Patient, NumericObservation
from graphs.models import GraphGrid, imageGraph
from django.http import HttpResponse
from graphs.ews import calculateEWS, chooseEWSColour
import datetime
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from os.path import join

dateformat = "%Y-%m-%d-%H-%M"

SCALE = 4
DOTSIZE = 1
print join(settings.FONTS_DIR, "Quicksand_Bold.otf")
SMALLFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Quicksand_Bold.otf"), 9 * SCALE)
MEDIUMFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Quicksand_Bold.otf"), 12 * SCALE)
LARGEFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Quicksand_Bold.otf"), 15 * SCALE)

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
    i = Image.new("RGB", 
                  (imagegraph.width * SCALE, 
                   imagegraph.height * SCALE), 
                  "white")
    draw = ImageDraw.Draw(i)
    #Right Border
    lb = imagegraph.left_border * SCALE
    rb = (imagegraph.width - imagegraph.right_border) * SCALE
    tb = imagegraph.top_border * SCALE
    bb = (imagegraph.height - imagegraph.bottom_border) * SCALE
    time_series = imagegraph.imagegraphtimeseries_set.all()
    graph_series = imagegraph.imagegraphseries_set.all()
    for ls in graph_series:
        for l in ls.imagegraphseriesline_set.all():
            pixel = ls.get_pos(l.value) * SCALE
            if l.linethickness:
                draw.line((lb, pixel, rb, pixel), 
                       width = int(imagegraph.linethickness * SCALE),
                       fill = l.line_colour)
            if l.othervalue:
                otherpixel = ls.get_pos(l.othervalue) * SCALE 
                draw.rectangle((lb, pixel, rb, otherpixel), 
                       fill = l.line_colour)
        sizeX, sizeY = draw.textsize(" " + ls.label, font = MEDIUMFONT)
        try: 
           v = str(NumericObservation.objects.filter(patient = patient, 
                                                     observation_type = ls.observation_type, 
                                                     datetime__lt = datetimenow)[0].value) + ls.observation_type.units
        except :
           v = "(%s)" % ls.observation_type.units
        
        drawlabel(draw, (rb, (ls.upper_pixel + ls.lower_pixel) * SCALE / 2 - sizeY / 2), " " + ls.label, ls.label_colour)
        draw.text((rb, (ls.upper_pixel + ls.lower_pixel) * SCALE / 2 + sizeY / 2), " " + v, fill="black", font = LARGEFONT)
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
        tlb = tlb - ts.width * SCALE
        if ts.left_axis:
            draw.line((tlb, tb, tlb, bb), 
                       width = int(imagegraph.linethickness) * SCALE,
                       fill = "black")
            for ls in graph_series:
                for l in ls.imagegraphseriesline_set.all():
                    if l.label:
                        options = {"font": SMALLFONT}
                        drawTickLabel(draw, 
                                      "%s" % l.value, 
                                      tlb, 
                                      ls.get_pos(l.value) * SCALE, 
                                      l.label_colour, 
                                      **options)
                        if l.othervalue:
                            drawTickLabel(draw, 
                                          "%s" % l.othervalue, 
                                          tlb, 
                                          ls.get_pos(l.othervalue) * SCALE, 
                                          l.label_colour, 
                                          **options)
        for ls in graph_series:
            for n in NumericObservation.objects.filter(patient = patient, 
                                                       observation_type = ls.observation_type, 
                                                       datetime__lt = enddatetime, 
                                                       datetime__gt = startdatetime
                                                       ):
                print ls.observation_type, n.datetime, n.value
                t = trb - ts.get_pixels(enddatetime - n.datetime.replace(tzinfo=None)) * SCALE
                y = ls.get_pos(n.value) * SCALE
                draw.ellipse((t - DOTSIZE * SCALE, y - DOTSIZE * SCALE, t + DOTSIZE * SCALE, y + DOTSIZE * SCALE), ls.line_colour)
    del draw
    response=HttpResponse(content_type='image/png')
    i.resize((imagegraph.width, 
              imagegraph.height), Image.ANTIALIAS).save(response, "PNG")
    return response

def drawlabel(draw, (x, y), label, colour):
    labels = label.split("__")
    x = x
    small = False # This probably needs fixing
    fonts = {True: SMALLFONT, False: MEDIUMFONT}
    offset = {True: 0.4, False: 0}
    for label in labels:
        sizeX, sizeY = draw.textsize(label, font = fonts[small])
        draw.text((x, y + offset[small] * sizeY), label, fill=colour, font = fonts[small])
        x = x + sizeX
        small = not(small)

def drawTickLabel(draw, string, x, y, colour, **options):
                        sizeX, sizeY = draw.textsize(string, **options)
                        x = x - sizeX / 2 
                        y = y - sizeY / 2
                        draw.rectangle((x - 1, y - 1, x + sizeX, y + sizeY), fill = "white")
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
        recentEWSCalc = calculateEWS( recentRR, recentSpO2, recentTemp, recentSBP, recentHR, 0, 0 )
        recentEWS = recentEWSCalc['EWS']
    except:
        recentEWS = "-"
    #choose a colour for the EWS
    try:
        EWSColour = chooseEWSColour( recentEWSCalc['EWS'], recentEWSCalc['EWSRedScore'] )
    except: 
        EWSColour = "EWSBlue"
    #Return patient, date and observation details
    return render(request, 'vitalsvis.html', {'patient': patient, 'datenow': datenow, 'timenow': timenow, 'datetimeoneday': datetimeoneday, 'datetimefivedays': datetimefivedays, 'datetimezerodays': datetimezerodays, 'recentRR': recentRR, 'recentSpO2': recentSpO2, 'recentTemp': recentTemp, 'recentSBP': recentSBP, 'recentDBP': recentDBP, 'recentHR': recentHR, 'recentEWS': recentEWS, 'EWSColour': EWSColour, 'width': 290, 'height': 90, 'bpheight': 150})
