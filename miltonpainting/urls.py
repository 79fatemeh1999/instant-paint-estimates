from django.urls import path

from . import views

app_name = 'miltonpainting'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
     # ex: /miltonpainting/5/bookingdone/
    path('<int:pk>/', views.bookingDone.as_view(), name='bookingdone'),
    # ex: /miltonpainting/5/estimateresults/
    path('<int:pk>/estimateresults/', views.estimateResults.as_view(), name='estimateresults'),
    # ex: /miltonpainting/estimate/
    path('estimate/', views.estimate, name='estimate'),
]