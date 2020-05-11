from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import HomeForm,BlockerForm,CampaignCeatorForm,HealthCheckerForm
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
#from .forms import BlockerForm
from .models import Blocker,Campaigns
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import re

#class HomeView(TemplateView):
#    template_name = 'campaigngenerator/home.html'

#    def get(self, request):
#        form = HomeForm()
#        return render(request, self.template_name, {'form': form})



def home(request):
    form = HomeForm()
    return render(request, 'campaigngenerator/home.html', {'form':form})

#def create(response):
#    form = HomeForm()
#    return render(response, "campaigngenerator/home.html", {'form':form})

#def campaigncreator(request):
#    form = CampaignCeator()
#    return render(request, 'campaigngenerator/campaigncreator.html', {'form':form})

def healthchecker(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/healthchecker.html')
    else:
        #test(request)
        #devices = HealthCheckerForm(request.POST)
        #if request.POST['devices']:
        #devices = request.POST['devices']
        devices = inputformat(request)
        devices = '|'.join(['-'.join(x) for x in devices])
        return render(request, 'campaigngenerator/viewhealthchecker.html', {'devices': devices})

def inputformat(request):
    devices = request.POST['devices']
    devices = re.sub('[,; |\'\"]', ' ', devices)
    data = []
    splitter = re.split('\r\n| |,|;',devices)
            #test = re.split('.',1)
    for item in splitter:
        item = item.split('.')[0].rstrip()
        if item !="":
            data.append(item)
    data.sort()
    data = [y for y in [x.split('-') for x in data]]
    return data

@login_required
def campaigncreator(request):
    #form = Campaigns()
    if request.method == 'GET':
        return render(request, 'campaigngenerator/campaigncreator.html')
    elif request.method == 'POST':
        form = CampaignCeatorForm(request.POST)
        if request.POST['devices']:
            data = inputformat(request)
            #devices = request.POST['devices']
            #devices = re.sub('[,; |\'\"]', ' ', devices)
#            data = []
#            splitter = re.split('\r\n| |,|;',devices)
            #test = re.split('.',1)
#            for item in splitter:
#                item = item.split('.')[0].rstrip()
#                if item !="":
#                    data.append(item)
#            data.sort()
#            data = [y for y in [x.split('-') for x in data]]

            for col in range(len(data[0]) -1,-1,-1):
                result = []
                def add_result():
                    result.append([])
                    #fulltext = result

                    if headstr:
                        result[-1] += headstr.split('-')
                    if len(list(findnum)) > 1:
                        result[-1] += [f'{findstr}({"|".join(sorted(findnum))})']
                    elif len(list(findnum)) == 1:
                        result[-1] += [f'{findstr}{findnum[0]}']
                    if tailstr:
                        result[-1] += tailstr.split('-')

                _headstr = lambda x, y: '-'.join(x[:y])
                _tailstr = lambda x, y: '-'.join(x[y + 1:])
                _findstr = lambda x: re.findall('(\D+)', x)[0] if re.findall('(\D+)', x) else ''
                _findnum = lambda x: re.findall('(\d+)', x)[0] if re.findall('(\d+)', x) else ''

                headstr = _headstr(data[0], col)
                tailstr = _tailstr(data[0], col)
                findstr = _findstr(data[0][col])
                findnum = []

                for row in data:
                    if headstr + findstr + tailstr != _headstr(row, col) + _findstr(row[col]) + _tailstr(row, col):
                      add_result()
                      headstr = _headstr(row, col)
                      tailstr = _tailstr(row, col)
                      findstr = _findstr(row[col])
                      findnum = []
                    if _findnum(row[col]) not in findnum:
                      findnum.append(_findnum(row[col]))

                else:
                    add_result()

                data = result[:]
                devices = ['-'.join(x) for x in result]

            reg = devices[0].split("-c1-")[0]
            blockers = Blocker.objects.filter(datecompleted__isnull=True)
            return render(request, 'campaigngenerator/viewcampaigns.html', {'devices':devices, 'blockers':blockers, 'reg':reg})
        else:
            return render(request, 'campaigngenerator/campaigncreator.html')

def allcampaigns(request):
    campaigns = Campaigns.objects.all()
    return render(request, 'campaigngenerator/allcampaigns.html', {'campaigns':campaigns})

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/signupuser.html', {'form':UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentblockers')
            except IntegrityError:
                return render(request, 'campaigngenerator/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose different username'})
        else:
            return render(request, 'campaigngenerator/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/loginuser.html', {'form':AuthenticationForm()})
    else:
        # Create a new user
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'campaigngenerator/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did NOT match'})
        else:
            login(request, user)
            return redirect('currentblockers')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createblocker(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/createblocker.html', {'form':BlockerForm()})
    else:
        try:
            form = BlockerForm(request.POST)
            newblocker = form.save(commit=False)
            newblocker.user = request.user
            newblocker.save()
            return redirect('currentblockers')
        except ValueError:
            return render(request, 'campaigngenerator/createblocker.html', {'form':BlockerForm(),'error':'BAD data passed in. Try again'})

@login_required
def currentblockers(request):
    blockers = Blocker.objects.filter(datecompleted__isnull=True)
    return render(request, 'campaigngenerator/currentblockers.html', {'blockers':blockers})

@login_required
def completedblockers(request):
    blockers = Blocker.objects.filter(datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'campaigngenerator/completedblockers.html', {'blockers':blockers})

@login_required
def allblockers(request):
    #if request.method == 'POST':
    blockers = Blocker.objects.all()
    return render(request, 'campaigngenerator/allblockers.html', {'blockers':blockers})

@login_required
def viewblocker(request, blocker_pk):
    blocker = get_object_or_404(Blocker, pk=blocker_pk)
    if request.method == 'GET':
        form = BlockerForm(instance=blocker)
        return render(request, 'campaigngenerator/viewblocker.html', {'blocker':blocker, 'form':form})
    else:
        try:
            form = BlockerForm(request.POST, instance=blocker)
            form.save()
            return redirect('currentblockers')
        except ValueError:
            return render(request, 'campaigngenerator/viewblocker.html', {'blocker':blocker, 'form':form,'error':'BAD data passed in. Try again'})

@login_required
def completeblocker(request, blocker_pk):
    blocker = get_object_or_404(Blocker, pk=blocker_pk)
    if request.method == 'POST':
        blocker.datecompleted = timezone.now()
        blocker.save()
        return redirect('currentblockers')

@login_required
def notcompleteblocker(request, blocker_pk):
    blocker = get_object_or_404(Blocker, pk=blocker_pk)
    if request.method == 'POST':
        blocker.datecompleted = None
        blocker.save()
        return redirect('currentblockers')

@login_required
def deleteblocker(request, blocker_pk):
    blocker = get_object_or_404(Blocker, pk=blocker_pk)
    if request.method == 'POST':
        blocker.delete()
        return redirect('currentblockers')
