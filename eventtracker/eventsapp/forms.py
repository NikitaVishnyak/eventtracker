from cities_light.models import City
from django import forms

from eventsapp.models import Events


class AddEventForm(forms.ModelForm):
    class Meta:
        model = Events
        fields = ['title', 'description', 'start_time', 'end_time', 'country', 'city', 'category']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'country': forms.Select(attrs={'id': 'id_country'}),
            'city': forms.Select(attrs={'id': 'id_city'}),
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # Отримати об'єкт request
        super().__init__(*args, **kwargs)
        country = self['country'].value()
        if country:
            self.fields['city'].queryset = City.objects.filter(country_id=country)
        else:
            self.fields['city'].queryset = City.objects.none()

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.request:
            instance.organizer = self.request.user  # Встановити організатора з об'єкта request
        if commit:
            instance.save()
        return instance

    def clean_city(self):
        city = self.cleaned_data.get('city')
        country = self.cleaned_data.get('country')
        if city and country and city.country != country:
            raise forms.ValidationError("City does not belong to selected country.")
        return city
