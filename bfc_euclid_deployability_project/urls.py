
from django.contrib import admin
from django.urls import path, include
#import campaigngenerator.views
from campaigngenerator import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    #path('count/', views.count, name='count'),

    # Auth
    path('signup/', views.signupuser, name='signupuser'),
    path('login/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # Blocker
    path('create/', views.createblocker, name='createblocker'),
    path('current/', views.currentblockers, name='currentblockers'),
    path('allblockers/', views.allblockers, name='allblockers'),
    path('completed/', views.completedblockers, name='completedblockers'),
    path('blocker/<int:blocker_pk>', views.viewblocker, name='viewblocker'),
    path('blocker/<int:blocker_pk>/complete', views.completeblocker, name='completeblocker'),
    path('blocker/<int:blocker_pk>/notcomplete', views.notcompleteblocker, name='notcompleteblocker'),
    path('blocker/<int:blocker_pk>/delete', views.deleteblocker, name='deleteblocker'),

    # Campaigns
    path('campaigncreator/', views.campaigncreator, name='campaigncreator'),
    path('allcampaigns/', views.allcampaigns, name='allcampaigns'),

    # Health Checker view
    path('healthchecker/', views.healthcheckerview, name='healthchecker'),


    # API View
    # Health CHecker
    path('healthcheckerapi/', views.HealthCheckerApi.as_view())





]
