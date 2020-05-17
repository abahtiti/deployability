
from django.contrib import admin
from django.urls import path, include
#import campaigngenerator.views
from campaigngenerator import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('summary/', views.summary, name='summary'),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),

    # dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Blocker
    path('create/', views.createblocker, name='createblocker'),
    path('current/', views.currentblockers, name='currentblockers'),
    path('criticalblockers/', views.criticalblockers, name='criticalblockers'),
    path('allblockers/', views.allblockers, name='allblockers'),
    path('completed/', views.completedblockers, name='completedblockers'),
    path('blocker/<int:blocker_pk>', views.viewblocker, name='viewblocker'),
    path('blocker/<int:blocker_pk>/complete', views.completeblocker, name='completeblocker'),
    path('blocker/<int:blocker_pk>/notcomplete', views.notcompleteblocker, name='notcompleteblocker'),
    path('blocker/<int:blocker_pk>/delete', views.deleteblocker, name='deleteblocker'),

    # Known Problems
    path('createkp/', views.createkp, name='createkp'),
    path('allkp/', views.allkp, name='allkp'),
    path('kp/<int:kp_pk>', views.viewkp, name='viewkp'),
    path('kp/<int:kp_pk>/delete', views.deletekp, name='deletekp'),


    # Campaigns
    path('campaigncreator/', views.campaigncreator, name='campaigncreator'),
    path('submitcampaign/', views.submitcampaign, name='submitcampaign'),
    #path('allcampaigns/', views.allcampaigns, name='allcampaigns'),

    # Health Checker view
    path('healthchecker/', views.healthcheckerview, name='healthchecker'),

    # nhschecker view
    path('nhschecker/', views.splitastemplateview, name='nhschecker'),

    # search
    path('search/', views.search, name='search'),


    # API View
    # Health CHecker
    path('healthcheckerapi/', views.HealthCheckerApi.as_view())







]
