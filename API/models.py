from django.db import models

class Station(models.Model):
    id_station = models.AutoField(primary_key=True)
    nama_stasiun = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.nama_stasiun
    
class PollutantData(models.Model):
    id_data = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='pollutant_data')
    tanggal = models.DateField()

    pm10 = models.FloatField(null=True, blank=True)
    pm25 = models.FloatField(null=True, blank=True)
    so2 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    o3 = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.station.nama_stasiun} - {self.tanggal}"
    
class MeteorologicalData(models.Model):
    id_data = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='meteorological_data')
    tanggal = models.DateField()

    temperatur_minimum = models.FloatField(null=True, blank=True)
    temperatur_maksimum = models.FloatField(null=True, blank=True)
    temperatur_rata = models.FloatField(null=True, blank=True)
    kelembapan_rata = models.FloatField(null=True, blank=True)
    curah_hujan = models.FloatField(null=True, blank=True)
    kecepatan_angin_maksimum = models.FloatField(null=True, blank=True)
    kecepatan_angin_rata = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.station.nama_stasiun} - {self.tanggal}"
    
class ModelMSSA(models.Model):
    id_model = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='modelmssa',null=True, blank=True)
    window_length = models.IntegerField()
    embedding_dimension = models.IntegerField()
    jumlah_komponen = models.IntegerField()
    lag_data = models.IntegerField()
    mse = models.FloatField()
    rmse = models.FloatField()
    mae = models.FloatField()
    akurasi = models.FloatField()

    def __str__(self):
        return f"MSSA Model #{self.id_model}"

class PredictionResult(models.Model):
    id_pred = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='predictions')
    model = models.ForeignKey(ModelMSSA, on_delete=models.SET_NULL, null=True, related_name='predictions')
    tanggal_prediksi = models.DateField()

    pm10_pred = models.FloatField(null=True, blank=True)
    pm25_pred = models.FloatField(null=True, blank=True)
    so2_pred = models.FloatField(null=True, blank=True)
    co_pred = models.FloatField(null=True, blank=True)
    o3_pred = models.FloatField(null=True, blank=True)
    no2_pred = models.FloatField(null=True, blank=True)
    indeks_kualitas_udara = models.CharField(max_length=40)

    def __str__(self):
        return f"Prediksi {self.station.nama_stasiun} ({self.tanggal_prediksi})"
    
class MapView(models.Model):
    id_view = models.AutoField(primary_key=True)
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='map_views')
    tanggal = models.DateField()

    pm10 = models.FloatField(null=True, blank=True)
    pm25 = models.FloatField(null=True, blank=True)
    so2 = models.FloatField(null=True, blank=True)
    co = models.FloatField(null=True, blank=True)
    o3 = models.FloatField(null=True, blank=True)
    no2 = models.FloatField(null=True, blank=True)
    indeks_kualitas_udara = models.CharField(max_length=20)

    def __str__(self):
        return f"MapView - {self.station.nama_stasiun} ({self.tanggal})"

class CorrelationAnalysis(models.Model):
    id_corr = models.AutoField(primary_key=True)
    pasangan_variabel = models.CharField(max_length=50)
    nilai_korelasi = models.FloatField()
    tingkat_kekuatan = models.CharField(max_length=30)
    tanggal_analisis = models.DateField()

    def __str__(self):
        return f"{self.pasangan_variabel} ({self.nilai_korelasi:.2f})"