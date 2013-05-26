from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'graphs.views.home', name='home'),
    url(r'^graphgrid/(.*)$', 'graphs.views.graphgrid', name='viewgrid'),
    url(r'^registerpatient$', 'patients.views.registerPatient', name='registerPatient'),
    url(r'^$', 'patients.views.patientObservation', name='patientObservation'),
    url(r'^getObs/([^/]*)/([^/]*)', 'patients.views.getObs', name='getObs'),
    url(r'^graph/(?P<mrn>[^/]*)/(?P<obs>[^/]*)/start(?P<start>[^/]*)/end(?P<end>[^/]*)/compass(?P<compass>[^/]*)/height(?P<height>[^/]*)/width(?P<width>[^/]*)/min(?P<min_>[^/]*)/max(?P<max_>[^/]*)/refmin(?P<refmin>[^/]*)/refmax(?P<refmax>[^/]*)$', 'patients.views.g', name="g"),
	url(r'^getVis/([^/]*)', 'graphs.views.vitalsVis', name='vitalsVis'),
    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)

from django.conf import settings

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )

