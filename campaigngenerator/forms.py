from django import forms
from django.forms import ModelForm
from .models import Blocker
from .models import Campaigns

class HomeForm(forms.Form):
    post = forms.CharField(label="post", max_length=200, widget=forms.Textarea)
    #check = forms.BooleanField()

    def decompress(self,value):
        if value:
            return value.split('')
        return [None, None]
        print(value)

class BlockerForm(ModelForm):
    class Meta:
        model = Blocker
        fields = ['title','body','important']

#class CampaignCeatorForm(forms.Form):
class CampaignCeatorForm(ModelForm):
    class Meta:
        model = Campaigns
        fields = ['devices']

class HealthCheckerForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    devices = forms.CharField()
