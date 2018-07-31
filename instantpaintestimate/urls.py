from django.urls import path

from . import views

app_name = 'instantpaintestimate'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    # ex: /instantpaintestimate/5/estimateresults/
    path('<int:estimate_id>/estimateresults/', views.estimateResults, name='estimateresults'),
    # ex: /instantpaintestimate/estimate/
    path('estimate/', views.estimate, name='estimate'),
]