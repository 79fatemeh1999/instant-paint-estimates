from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import PaintEstimate, PaintEstimateUser
from .forms import PaintEstimateForm
from .helpers import cleanPaintValues, calculatePaintEstimatePrice, sendEmail
from instantpaintestimate import models
from django.views import generic
from django.shortcuts import render
from django.urls import reverse
import pdb

class index(generic.ListView):
    """
    Displays the home page 
    """
    model = PaintEstimateUser
    template_name = 'instantpaintestimate/index.html'


def estimate(request):
    """
    Shows the estimate form used to submit estimates 
    """
    if request.method == 'GET':
        form = PaintEstimateForm()
    else:
        # A POST request: Handle Form Upload
        # Bind data from request.POST into an EstimateForm
        form = PaintEstimateForm(request.POST, request.FILES)

        # If data is valid, proceeds to create a new db entry and redirect the user
        if form.is_valid():
            values = cleanPaintValues(form)
            estimate_company = PaintEstimate.objects.all().first()
            estimate_cost = calculatePaintEstimatePrice(values, estimate_company)
            
            estimate = PaintEstimateUser.objects.create(
                                                     bedrooms=values['bedrooms'],
                                                     master_bedroom = values['master_bedroom'],
                                                     bathrooms=values['bathrooms'],
                                                     master_bathroom=values['master_bathroom'],
                                                     living_room=values['living_room'],
                                                     kitchen=values['kitchen'],
                                                     ceiling=values['ceiling_painted'],
                                                     ceiling_height=values['ceiling_height'],
                                                     ceiling_trim=values['ceiling_trim'],
                                                     baseboard_trim=values['baseboard_trim'],
                                                     estimate_cost=estimate_cost,
                                                     email=values['email'],
                                                     name=values['name'],
                                                     other_rooms=values['other_rooms'],
                                                     stairways=values['stairways'],
                                                     phone=values['phone'],
                                                     estimate_date=form.cleaned_data['estimate_date'])

            estimate.save()

            # send an email with the details of the estimate
            sendEmail(estimate, estimate_company)
            return HttpResponseRedirect(reverse('instantpaintestimate:estimateresults', args=(estimate.id,)))

    return render(request, 'instantpaintestimate/estimate.html', {
        'form': form,
    })
    
def estimateResults(request, estimate_id):
    """
    Display the results of the paint estimate  
    """
    estimate = PaintEstimateUser.objects.filter(id=estimate_id).first()
    
    return render(request, 'instantpaintestimate/estimateresults.html', {
    'estimate': estimate,
    })

