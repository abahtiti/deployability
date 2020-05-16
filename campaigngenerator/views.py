from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import HomeForm,BlockerForm,CampaignCeatorForm,HealthCheckerForm
from django.views.generic import TemplateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .models import Blocker,Campaigns
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from campaigngenerator import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import timedelta, date, datetime
import re

#class HomeView(TemplateView):
#    template_name = 'campaigngenerator/home.html'

#    def get(self, request):
#        form = HomeForm()
#        return render(request, self.template_name, {'form': form})



def home(request):
    form = HomeForm()
    return render(request, 'campaigngenerator/home.html', {'form':form})

# Prepare Input Data format
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

# Health Checker is to check device management eth0, NSM_DIFF, device status(down/shifted)
# Health Checker Template
def healthcheckerview(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/healthchecker.html')
    else:
        devices = HealthCheckerForm(request.POST)
        devices = inputformat(request)
        if devices != []:
            devices = ['-'.join(x) for x in devices]
            length = 'Number of devices: {}'.format(len(devices))
            devices = '|'.join(devices)
            command = './check_port -p "name:/{}/"'.format(devices)
            return render(request, 'campaigngenerator/viewhealthchecker.html', {'command': command,'length':length})
        else:
            return render(request, 'campaigngenerator/healthchecker.html')


# Heatlth Checker API
class HealthCheckerApi(APIView):
    """Health Checker API View"""
    serializer_class = serializers.HealthCheckerSerializer

    def get(self, request, format=None):
        """Returns a list of APIView features"""
        an_apiview = [
            'Uses HTTP methods as function (get, post)',
            'Use the command given to check device management eth0, NSM_DIFF, device status(down/shifted)',
        ]
        return Response({'message': 'HealthCheckerApi', 'an_apiview': an_apiview})

    def post(self, request):
        """Provide a command with input devices"""
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            devices = serializer.validated_data.get('devices')
            devices = inputformat(request)
            devices = '|'.join(['-'.join(x) for x in devices])
            command = f'test {devices} test'
            return Response({'Command': command})

# Splitter is to split devices as per predefined template,row/columun
# Splitter Template
def splitastemplateview(request):
    if request.method == 'GET':
        return render(request, 'campaigngenerator/nhschecker.html')
    else:
        devices = inputformat(request)
        if devices != []:
            devices = ['-'.join(x) for x in devices]
            reg = re.split('-c1-|-e1-',devices[0])[0]
            blockers = Blocker.objects.filter(datecompleted__isnull=True)
            r1_2_3_lst,r4_5_6_lst,r7_8_9_lst,r10_11_12_lst,r13_14_15_lst,r16_lst,r1_5_9_t1_lst,r2_10_13_t1_lst,r3_6_14_t1_lst,r4_7_11_t1_lst,r8_12_15_t1_lst,r16_t1_lst = [[] for _ in range(12)]
            for device in devices:
                if (re.search(r'\bt2-r1\b',device) or re.search(r'\bs.*-r1\b',device)
                    or re.search(r'\bt2-r3\b',device) or re.search(r'\bs.*-r3\b',device)
                    or re.search(r'\bt2-r2\b',device) or re.search(r'\bs.*-r2\b',device)):
                    r1_2_3_lst.append(device)
                elif (re.search(r'\bt2-r4\b',device) or re.search(r'\bs.*-r4\b',device)
                      or re.search(r'\bt2-r5\b',device) or re.search(r'\bs.*-r5\b',device)
                      or re.search(r'\bt2-r6\b',device) or re.search(r'\bs.*-r6\b',device)):
                    r4_5_6_lst.append(device)
                elif (re.search(r'\bt2-r7\b',device) or re.search(r'\bs.*-r7\b',device)
                      or re.search(r'\bt2-r8\b',device) or re.search(r'\bs.*-r8\b',device)
                      or re.search(r'\bt2-r9\b',device) or re.search(r'\bs.*-r9\b',device)):
                    r7_8_9_lst.append(device)
                elif (re.search(r'\bt2-r10\b',device) or re.search(r'\bs.*-r10\b',device)
                      or re.search(r'\bt2-r11\b',device) or re.search(r'\bs.*-r11\b',device)
                      or re.search(r'\bt2-r12\b',device) or re.search(r'\bs.*-r12\b',device)):
                    r10_11_12_lst.append(device)
                elif (re.search(r'\bt2-r13\b',device) or re.search(r'\bs.*-r13\b',device)
                      or re.search(r'\bt2-r14\b',device) or re.search(r'\bs.*-r14\b',device)
                      or re.search(r'\bt2-r15\b',device) or re.search(r'\bs.*-r15\b',device)):
                    r13_14_15_lst.append(device)
                elif re.search(r'\bt2-r16\b',device) or re.search(r'\bs.*-r16\b',device):
                    r16_lst.append(device)
                elif (re.search(r'\bt1-r1\b',device)
                    or re.search(r'\bt1-r3\b',device)
                    or re.search(r'\bt1-r5\b',device)):
                    r1_5_9_t1_lst.append(device)
                elif (re.search(r'\bt1-r2\b',device)
                      or re.search(r'\bt1-r10\b',device)
                      or re.search(r'\bt1-r13\b',device)):
                    r2_10_13_t1_lst.append(device)
                elif (re.search(r'\bt1-r3\b',device)
                      or re.search(r'\bt1-r6\b',device)
                      or re.search(r'\bt1-r14\b',device)):
                    r3_6_14_t1_lst.append(device)
                elif (re.search(r'\bt1-r4\b',device)
                      or re.search(r'\bt1-r7\b',device)
                      or re.search(r'\bt1-r11\b',device)):
                    r4_7_11_t1_lst.append(device)
                elif (re.search(r'\bt1-r8\b',device)
                      or re.search(r'\bt1-r12\b',device)
                      or re.search(r'\bt1-r15\b',device)):
                    r8_12_15_t1_lst.append(device)
                elif re.search(r'\bt1-r16\b',device):
                    r16_t1_lst.append(device)
            def printout(group):
                return("./nhs_deployable_group.py device_deployment --devices {} --operation concurrent_shift".format(",".join(group)))
            rsdict = {}
            rsdict.update( {'r1_2_3_lst' : printout(r1_2_3_lst)} ) if r1_2_3_lst else 0
            rsdict.update( {'r4_5_6_lst' : printout(r4_5_6_lst)} ) if r4_5_6_lst else 0
            rsdict.update( {'r7_8_9_lst' : printout(r7_8_9_lst)} ) if r7_8_9_lst else 0
            rsdict.update( {'r10_11_12_lst' : printout(r10_11_12_lst)} ) if r10_11_12_lst else 0
            rsdict.update( {'r13_14_15_lst' : printout(r13_14_15_lst)} ) if r13_14_15_lst else 0
            rsdict.update( {'r16_lst' : printout(r16_lst)} ) if r16_lst else 0
            rsdict.update( {'r1_5_9_t1_lst' : printout(r1_5_9_t1_lst)} ) if r1_5_9_t1_lst else 0
            rsdict.update( {'r2_10_13_t1_lst' : printout(r2_10_13_t1_lst)} ) if r2_10_13_t1_lst else 0
            rsdict.update( {'r3_6_14_t1_lst' : printout(r3_6_14_t1_lst)} ) if r3_6_14_t1_lst else 0
            rsdict.update( {'r4_7_11_t1_lst' : printout(r4_7_11_t1_lst)} ) if r4_7_11_t1_lst else 0
            rsdict.update( {'r8_12_15_t1_lst' : printout(r8_12_15_t1_lst)} ) if r8_12_15_t1_lst else 0
            rsdict.update( {'r16_t1_lst' : printout(r16_t1_lst)} ) if r16_t1_lst else 0

            return render(request, 'campaigngenerator/viewnhschecker.html', {'rsdict':rsdict,'reg':reg,'blockers':blockers})
        else:
            return render(request, 'campaigngenerator/nhschecker.html')

def merge(data):
    data = [y for y in [x.split('-') for x in data]]
    for col in range(len(data[0]) -1,-1,-1):
        result = []
        def add_result():
            result.append([])
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
    return ['-'.join(x) for x in result]

def campaigncreator(request):
    #form = Campaigns()
    if request.method == 'GET':
        return render(request, 'campaigngenerator/campaigncreator.html')
    elif request.method == 'POST':
        form = CampaignCeatorForm(request.POST)
        if request.POST['devices']:
            data = inputformat(request)
            data = ['-'.join(x) for x in data]
            reg = re.split('-c1-|-e1-',data[0])[0]
            blockers = Blocker.objects.filter(datecompleted__isnull=True)
            t1data = [element for element in data if "-t1-r" in element]
            t2data = [element for element in  data if "-t2-r" in element]
            spinedata = [element for element in data if "-c1-s" in element]
            mixingt1_s_error = ''
            create = ''
            if spinedata:
                spinedata = '|'.join(map(str,merge(spinedata)))
            if t2data:
                t2data = '|'.join(map(str,merge(t2data)))
            if t1data:
                t1data = '|'.join(map(str,merge(t1data)))
            deadline = date.today() + timedelta(days=4)
            if t2data and spinedata:
                alldevices = t2data + "|" + spinedata
                if t1data:
                    alldevices = t1data + "|" + alldevices
                create = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign create -n "{}#name:/{}/" --deadline "{} 00:59" --template alfred-bfc-columnar-3-column-1-row-batching --tags {}-c1_DNO_CONTRACTORS p100_chase'.format(alldevices[0:3],alldevices,deadline,alldevices.split("-c1-")[0])
            elif spinedata and not t2data and not t1data:
                alldevices = spinedata
                create = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign create -n "{}#name:/{}/" --deadline "{} 00:59" --template alfred-bfc-columnar-spine-row-based-deployment --tags {}-c1_DNO_CONTRACTORS p100_chase'.format(alldevices[0:3],alldevices,deadline,alldevices.split("-c1-")[0])
            elif t2data and t1data and not spinedata:
                alldevices = t2data + "|" + t1data
                create = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign create -n "{}#name:/{}/" --deadline "{} 00:59" --template alfred-bfc-columnar-3-column-1-row-batching --tags {}-c1_DNO_CONTRACTORS p100_chase'.format(alldevices[0:3],alldevices,deadline,alldevices.split("-c1-")[0])
            elif t1data and not spinedata:
                alldevices = t1data
                create = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign create -n "{}#name:/{}/" --deadline "{} 00:59" --template alfred-bfc-columnar-3-column-1-row-batching --tags {}-c1_DNO_CONTRACTORS p100_chase'.format(alldevices[0:3],alldevices,deadline,alldevices.split("-c1-")[0])
            elif t2data and not spinedata:
                alldevices = t2data
                create = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign create -n "{}#name:/{}/" --deadline "{} 00:59" --template alfred-bfc-columnar-3-column-1-row-batching --tags {}-c1_DNO_CONTRACTORS p100_chase'.format(alldevices[0:3],alldevices,deadline,alldevices.split("-c1-")[0])
            elif t1data and spinedata and not t2data:
                mixingt1_s_error = 'ERROR!, Mixing T1s and Spines will result in spines only deployment which will be rejected, please split it into two campaigns'
                return render(request, 'campaigngenerator/campaigncreator.html', {'mixingt1_s_error':mixingt1_s_error})
            elif create =='':
                return render(request, 'campaigngenerator/campaigncreator.html',{'errorbadformat':'ERROR! Please enter valid device name format'})
            return render(request, 'campaigngenerator/viewcampaigns.html', {'create':create,'reg':reg,'blockers':blockers})
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

def dashboard(request):
    allblockers = int(Blocker.objects.all().count())
    closedblockers = int(Blocker.objects.filter(datecompleted__isnull=False).count())
    activeblockers = int(Blocker.objects.filter(datecompleted__isnull=True).count())
    if not activeblockers:
        activeblockers = 0
    varA = ['All Blockers', 'Active Blockers','Closed Blockers']
    varB = [allblockers,activeblockers,closedblockers]
    context = {'test':'test','varA':varA,'varB':varB}
    return render(request,'campaigngenerator/dashboard.html',context)

def submitcampaign(request):
    campaign = request.POST['hid']
    if "http" in campaign:
        campaign_id = campaign.split("campaign/")[-1]
        #campaign_id = '/apollo/env/NetworkDeviceCampaignServiceCLI/bin/campaign-service campaign approve -c {} -a neteng-l1-approver -m "Looks good to me."'.format(campaign_id)

    else:
        return render(request,'campaigngenerator/viewcampaigns.html',{'errorformat':'ERROR!Please enter a valid URL'})
    return render(request,'campaigngenerator/viewcampaigns.html',{'hid':campaign_id})
