from django import forms
from .models import PollutantData, MeteorologicalData, Station

class PollutantDataForm(forms.ModelForm):
    class Meta:
        model = PollutantData
        fields = ['station', 'tanggal', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3']
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['station'].queryset = Station.objects.exclude(
            nama_stasiun__in=[
                "Kemayoran",
                "Halim Perdana Kusuma",
                "Maritim Tanjung Priok",
            ]
        )
        for visible in self.visible_fields():
            visible.field.widget.attrs.update({
                'class': (
                    'w-full border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-900 '
                    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 '
                    'placeholder-gray-400 transition'
                )
            })

class MeteorologicalDataForm(forms.ModelForm):
    class Meta:
        model = MeteorologicalData
        fields = [
            'station', 'tanggal', 'temperatur_minimum', 'temperatur_maksimum',
            'temperatur_rata', 'kelembapan_rata', 'curah_hujan',
            'kecepatan_angin_maksimum', 'kecepatan_angin_rata'
        ]
        widgets = {'tanggal': forms.DateInput(attrs={'type': 'date'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['station'].queryset = Station.objects.filter(
            nama_stasiun__in=[
                "Kemayoran",
                "Halim Perdana Kusuma",
                "Maritim Tanjung Priok",
            ]
        )

        for visible in self.visible_fields():
            visible.field.widget.attrs.update({
                'class': (
                    'w-full border border-gray-800 rounded-lg px-3 py-2 text-sm text-gray-900 '
                    'focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 '
                    'placeholder-gray-400 transition'
                )
            })