from actionkit.models import CoreUser
from datetime import datetime
from django import forms
from django.contrib.localflavor.us import forms as usforms
from django.utils.translation import ugettext_lazy as _

class EventForm(forms.Form):
    title = forms.CharField(label=_("Title"), required=False)
    date = forms.DateField(label=_("Date"), required=False)
    time = forms.TimeField(label=_("Time"), required=False)

    venue = forms.CharField(label=_("Venue"), required=True)
    address = forms.CharField(label=_("Address"), required=True)
    city = forms.CharField(label=_("City"), required=True)
    state = usforms.USStateField(label=_("State"), required=True)
    zip = usforms.USZipCodeField(label=_("ZIP"), required=True)

    max_attendees = forms.IntegerField(label=_("Max Attendees"), required=True)
    host = forms.EmailField(label=_("Host's Email Address"), required=True)

    public_description = forms.CharField(label=_("Description"), required=False, widget=forms.Textarea())
    directions = forms.CharField(label=_("Directions"), required=False, widget=forms.Textarea())

    def clean_host(self):
        host = self.cleaned_data['host']
        try:
            user = CoreUser.objects.using("ak").get(email=host)
        except CoreUser.DoesNotExist:
            raise forms.ValidationError(_("No core_user exists with email %(email)s") % {'email': host})
        return user

    def clean(self):
        try:
            data = self.build_event_struct()
        except:
            pass
        else:
            self.event_struct = data
        return self.cleaned_data

    def build_event_struct(self):
        data = {}
        for key in "title venue city state zip max_attendees".split():
            data[key] = self.cleaned_data.get(key)
        for key in "directions public_description".split():
            if key in self.cleaned_data and self.cleaned_data.get(key).strip():
                data[key] = self.cleaned_data.get(key)
        data['creator_id'] = self.cleaned_data['host'].id
        data['address1'] = self.cleaned_data['address']        
        data['starts_at'] = datetime.combine(self.cleaned_data['date'], self.cleaned_data['time'])
        return data
