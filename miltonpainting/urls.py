from django.urls import path

from . import views

app_name = 'miltonpainting'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    # ex: /miltonpainting/5/estimateresults/
    path('<int:estimate_id>/estimateresults/', views.estimateResults, name='estimateresults'),
    # ex: /miltonpainting/estimate/
    path('estimate/', views.estimate, name='estimate'),
]