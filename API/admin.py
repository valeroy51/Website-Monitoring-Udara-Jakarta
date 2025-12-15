from django.contrib import admin

from .models import *

admin.site.register(Station)
admin.site.register(PollutantData)
admin.site.register(MeteorologicalData)
admin.site.register(ModelMSSA)
admin.site.register(PredictionResult)
admin.site.register(MapView)
admin.site.register(CorrelationAnalysis)