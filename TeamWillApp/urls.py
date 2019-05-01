"""TeamWill URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    #path('rest-auth/', include('rest_auth.urls')),
    #path('rest-auth/registration/', include('rest_auth.registration.urls')),
    path('type-credit', TypeCreditAPI.as_view()),
    path('type-credit/<int:id>', TypeCreditByIDAPI.as_view()),
    path('champ-credit', ChampCreditAPI.as_view()),
    path('dossier-prospect', DossierProspectAPI.as_view()),
    path('simulation-echeance', SimulationEcheanceAPI.as_view()),
    path('historique-prospect', HistoriqueProspectAPI.as_view()),
    path('demande-credit/<int:DCRID>/<int:DPRID>/<int:TCID>', DemandeCreditAPI.as_view()),
    path('doc-credit/<int:id>', DocumentByIDCredit.as_view()),
    path('list-demande', ListDemande.as_view()),
    path('list-document', ListDocumentDemande.as_view()),
    path('update-etat/<int:id>', UpdateETAT.as_view()),
    path('calcul-score/<int:id>/<int:DMID>', CalculateScoreAPI.as_view()),
    path('registration', Registration.as_view()),
    path('statistique', StatistiqueSimulation.as_view()),
    path('statistique-demande', StatistiqueDemandeCredit.as_view()),
    path('statistique-accepte', StatistiqueDemandeCreditAccepte.as_view()),
    path('login', LoginAPI.as_view())
]
