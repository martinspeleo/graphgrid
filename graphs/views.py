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
DOTSIZE = 1.5
SMALLFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Nunito-Bold.ttf"), 8 * SCALE)
MEDIUMFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Nunito-Bold.ttf"), 12 * SCALE)
LARGEFONT = ImageFont.truetype(join(settings.FONTS_DIR, "Nunito-Bold.ttf"), 15 * SCALE)
DATETIMENOW = datetime.datetime(2010,11, 1, 0, 59)

def home(request):
    graphgrids = GraphGrid.objects.all()
    return render(request, 'graphgrids.html', {'graphgrids': graphgrids})

def graphgrid(request, graphgrid):
    graphgrid = get_object_or_404(GraphGrid, name = graphgrid)
    return render(request, 'graphgrid.html', {'graphgrid': graphgrid})

def image_graph(request, mrn, graph_name):

    datetimenow = DATETIMENOW
    patient = get_object_or_404(Patient, mrn = mrn)
    imagegraph = get_object_or_404(imageGraph, name = graph_name)
    i = Image.new("RGB", 
                  (imagegraph.width * SCALE, 
                   imagegraph.height * SCALE), 
                  "white")
    draw = ImageDraw.Draw(i)
    
    #Find borders
    lb = imagegraph.left_border * SCALE
    rb = (imagegraph.width - imagegraph.right_border) * SCALE
    tb = imagegraph.top_border * SCALE
    bb = (imagegraph.height - imagegraph.bottom_border) * SCALE
    
    #Get Series
    time_series = imagegraph.imagegraphtimeseries_set.all()
    graph_series = imagegraph.imagegraphseries_set.all()
    
    #Draw day lines
    startdatetime = datetimenow
    tlb = rb
    for ts in time_series:
        enddatetime = startdatetime
        startdatetime = enddatetime - datetime.timedelta(ts.time_period_days)
        trb = tlb
        tlb = tlb - ts.width * SCALE
        previousmidnight = datetime.datetime(enddatetime.year, enddatetime.month, enddatetime.day)
        while previousmidnight > startdatetime:
            xpos = trb - ts.get_pixels(enddatetime - previousmidnight) * SCALE
            draw.line((xpos, tb, xpos, bb), width = SCALE, fill="#dddddd")
            previousmidnight = previousmidnight - datetime.timedelta(1)

    #Draw Series Lines and Labels
    slb = tb
    for ls in graph_series:
        stb = slb
        slb = stb + ls.pixel_height * SCALE
        for l in ls.imagegraphseriesline_set.all():
            pixel = slb - ls.get_pos(l.value) * SCALE
            if l.linethickness:
                draw.line((lb, pixel, rb, pixel), 
                       width = int(imagegraph.linethickness * SCALE),
                       fill = l.line_colour)
            if l.othervalue:
                otherpixel = slb - ls.get_pos(l.othervalue) * SCALE 
                draw.rectangle((lb, pixel, rb, otherpixel), 
                       fill = l.line_colour)
        try: 
           v = ("%%0.%df" % ls.decimal_places) % NumericObservation.objects.filter(
                                                     patient = patient, 
                                                     observation_type = ls.observation_type, 
                                                     datetime__lt = datetimenow).order_by("-datetime")[0].value
        except :
           v = "-"

        labelSizeX, labelSizeY = draw.textsize(" " + ls.label, font = MEDIUMFONT)
        valueSizeX, valueSizeY = draw.textsize(" " + v, font = LARGEFONT)    
        centralY = stb + ls.pixel_height * SCALE / 2    
        if ls.other_observation_type:
            try: 
               ov = ("%%0.%df" % ls.decimal_places) % NumericObservation.objects.filter(
                                                          patient = patient, 
                                                          observation_type = ls.other_observation_type, 
                                                          datetime__lt = datetimenow).order_by("-datetime")[0].value
            except :
               ov = "-"
            spaceSizeX, spaceSizeY = draw.textsize(" ", font = LARGEFONT)  
            drawLabel(draw, (rb, centralY - labelSizeY - valueSizeY / 2), " " + ls.label, ls.label_colour)
            drawValue(draw, (rb, centralY - valueSizeY / 2), v, "", ls.label_colour, imagegraph.right_border * SCALE)
            draw.line((rb + spaceSizeX, centralY + valueSizeY / 2, rb + valueSizeX, centralY + valueSizeY / 2), width = SCALE, fill="#dddddd")
            drawValue(draw, (rb, centralY + valueSizeY / 2), ov, ls.observation_type.units, ls.label_colour, imagegraph.right_border * SCALE)
        else:
            drawLabel(draw, (rb, centralY - labelSizeY), " " + ls.label, ls.label_colour)
            drawValue(draw, (rb, centralY), v, ls.observation_type.units, ls.label_colour, imagegraph.right_border * SCALE)
    #Draw Line representing current time
    if imagegraph.now_axis:
         draw.line((rb, tb, rb, bb), 
              width = int(imagegraph.linethickness),
              fill = "black")
         nowstring = datetimenow.strftime("%Y-%m-%d %H:%M")
         sizeX, sizeY = draw.textsize(nowstring, font = MEDIUMFONT)
         if sizeX < imagegraph.right_border * SCALE:
            x = rb - sizeX / 2
         else:
            x = imagegraph.width * SCALE - sizeX
         #draw.text((x, tb - sizeY), nowstring, fill="#bbbbbb", font = MEDIUMFONT)
    # Draw Data
    startdatetime = datetimenow
    tlb = rb
    for ts in time_series:
        enddatetime = startdatetime
        startdatetime = enddatetime - datetime.timedelta(ts.time_period_days)
        trb = tlb
        tlb = tlb - ts.width * SCALE
        sizeX, sizeY = draw.textsize(ts.label, font = MEDIUMFONT)
        draw.text((tlb - sizeX / 2, tb - sizeY), ts.label, fill="#bbbbbb", font = MEDIUMFONT)
        if ts.left_axis:
            draw.line((tlb, tb, tlb, bb), 
                       width = int(imagegraph.linethickness) * SCALE,
                       fill = "black")
            slb = tb
            for ls in graph_series:
                stb = slb
                slb = stb + ls.pixel_height * SCALE
                for l in ls.imagegraphseriesline_set.all():
                    if l.label:
                        options = {"font": SMALLFONT}
                        drawTickLabel(draw, 
                                      ("%%0.%df" % ls.decimal_places) % l.value, 
                                      tlb, 
                                      slb - ls.get_pos(l.value) * SCALE, 
                                      l.label_colour, 
                                      **options)
                        if l.othervalue:
                            drawTickLabel(draw, 
                                          ("%%0.%df" % ls.decimal_places) % l.othervalue, 
                                          tlb, 
                                          slb - ls.get_pos(l.othervalue) * SCALE, 
                                          l.label_colour, 
                                          **options)
        slb = tb
        for ls in graph_series:
          stb = slb
          slb = stb + ls.pixel_height * SCALE
          if ls.other_observation_type:
            p = [(trb - ts.get_pixels(enddatetime - n.datetime.replace(tzinfo=None)) * SCALE, slb - ls.get_pos(n.value) * SCALE) 
                 for n in NumericObservation.objects.filter(patient = patient, 
                                                       observation_type = ls.observation_type, 
                                                       datetime__lt = enddatetime, 
                                                       datetime__gt = startdatetime).order_by("datetime")]
            o = [(trb - ts.get_pixels(enddatetime - n.datetime.replace(tzinfo=None)) * SCALE, slb - ls.get_pos(n.value) * SCALE)
                 for n in NumericObservation.objects.filter(patient = patient, 
                                                       observation_type = ls.other_observation_type, 
                                                       datetime__lt = enddatetime, 
                                                       datetime__gt = startdatetime).order_by("datetime")]
            while bool(p) or bool(o):
                if p and o and p[0][0] == o[0][0]:
                  tp, yp = p.pop(0)
                  to, yo = o.pop(0)
                  draw.line((to, yo, tp, yp), 
                       width = int(imagegraph.linethickness * SCALE),
                       fill = ls.line_colour)  
                elif p and (not o or p[0][0] < o[0][0]):
                  tp, yp = p.pop(0)
                  draw.ellipse((tp - DOTSIZE * SCALE, yp - DOTSIZE * SCALE, tp + DOTSIZE * SCALE, yp + DOTSIZE * SCALE), ls.line_colour)
                else:
                  to, yo = o.pop(0)
                  draw.ellipse((to - DOTSIZE * SCALE, yo - DOTSIZE * SCALE, to + DOTSIZE * SCALE, yo + DOTSIZE * SCALE), ls.line_colour)
          else:
            for n in NumericObservation.objects.filter(patient = patient, 
                                                       observation_type = ls.observation_type, 
                                                       datetime__lt = enddatetime, 
                                                       datetime__gt = startdatetime
                                                       ):
                t = trb - ts.get_pixels(enddatetime - n.datetime.replace(tzinfo=None)) * SCALE
                y = slb - ls.get_pos(n.value) * SCALE
                draw.ellipse((t - DOTSIZE * SCALE, y - DOTSIZE * SCALE, t + DOTSIZE * SCALE, y + DOTSIZE * SCALE), ls.line_colour)
    del draw
    response=HttpResponse(content_type='image/png')
    i.resize((imagegraph.width, 
              imagegraph.height), Image.ANTIALIAS).save(response, "PNG")
    return response

def drawLabel(draw, (x, y), label, colour):
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

def drawValue(draw, (x, y), value, units, colour, maxWidth):
    valSizeX, valSizeY = draw.textsize(" " + value, font = LARGEFONT)
    draw.text((x, y), " " + value, fill="black", font = LARGEFONT)
    unitsSizeX, unitsSizeY = draw.textsize(units, font = SMALLFONT) 
    if valSizeX + unitsSizeX < maxWidth:
        unitX = x + valSizeX
        unitY = y + 0.9 * valSizeY - unitsSizeY
    else:
        unitX = x + maxWidth - unitsSizeX
        unitY = y + valSizeY
    draw.text((unitX, unitY), units, fill=colour, font = SMALLFONT)

def vitalsVis(request, mrn):
    patient = get_object_or_404(Patient, mrn = mrn)
	#Calculate the date/time limits for day lines + graph separation
    datetimenow = DATETIMENOW 
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
    try: 
        recentConciousLevel = "%0.f" % NumericObservation.objects.filter( patient = patient, observation_type__name = "Concious Level" ).order_by("-datetime")[0].value
    except:
        recentConciousLevel = "-"
	#calculate EWS
    try: 
        recentEWSCalc = calculateEWS( recentRR, recentSpO2, recentTemp, recentSBP, recentHR, recentConciousLevel, 0 )
        recentEWS = recentEWSCalc['EWS']
    except:
        recentEWS = "-"
    #choose a colour for the EWS
    try:
        EWSColour = chooseEWSColour( recentEWSCalc['EWS'], recentEWSCalc['EWSRedScore'] )
    except: 
        EWSColour = "EWSBlue"
    #Return patient, date and observation details
    return render(request, 'vitalsvis.html', {'patient': patient, 'datenow': datenow, 'timenow': timenow, 'recentEWS': recentEWS, 'EWSColour': EWSColour, 'width': 620, 'height': 510, 'bpheight': 150})
