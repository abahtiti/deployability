from django import forms
from django.forms import ModelForm
from .models import Blocker,Campaigns,KnownProblems

#class HomeForm(forms.Form):
#    post = forms.CharField(label="post", max_length=200, widget=forms.Textarea)
    #check = forms.BooleanField()

#    def decompress(self,value):
#        if value:
#            return value.split('')
#        return [None, None]
#        print(value)

class DateInput(forms.DateInput):
    input_type = 'date'

class BlockerForm(ModelForm):
    class Meta:
        model = Blocker
        widgets = {'duedate': DateInput()}
        fields = ['title','body','duedate','important']

class KnownProblemsForm(ModelForm):
    class Meta:
        model = KnownProblems
        fields = ['title','body']

#class CampaignCeatorForm(forms.Form):
class CampaignCeatorForm(ModelForm):
    class Meta:
        model = Campaigns
        fields = ['devices']

class HealthCheckerForm(forms.Form): #Note that it is not inheriting from forms.ModelForm
    devices = forms.CharField()
