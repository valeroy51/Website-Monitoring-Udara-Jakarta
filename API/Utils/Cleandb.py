import os
import django
import sys
from setup import setup
setup()

from API.models import (
    PollutantData, MeteorologicalData,
    ModelMSSA, PredictionResult,
    CorrelationAnalysis, Station, MapView
)

print("Membersihkan database...")

PollutantData.objects.all().delete()
MeteorologicalData.objects.all().delete()
ModelMSSA.objects.all().delete()
PredictionResult.objects.all().delete()
CorrelationAnalysis.objects.all().delete()
Station.objects.all().delete()
MapView.objects.all().delete()

print("Semua data berhasil dihapus!")
