from django.db import models
from importlib import import_module
from django.utils.timezone import now

class PaintEstimate(models.Model):

# Allows the setting of the company specific info  

    #def __str__(self):
    #   return self.company_name

    company_name = models.CharField(default='Fluid Estimates', max_length=200,
                                    help_text='Name of your business')
    email = models.CharField(default='', max_length=200,
                             help_text='Email of your business')

    phone = models.CharField(default='', max_length=200,
                             help_text='Phone number of your business')

    bedroom_price = models.IntegerField(default=0,
                                        help_text='Cost to paint a standard bedroom')
    master_bedroom_price = models.IntegerField(default=0,
                                               help_text='Cost to paint a master bedroom')
    bathroom_price = models.IntegerField(default=0,
                                         help_text='Cost to paint a standard bathroom')
    master_bathroom_price = models.IntegerField(default=0,
                                                help_text='Cost to paint a master bathroom')
    living_room_price = models.IntegerField(default=0,
                                            help_text='Cost to paint a living room')
    kitchen_price = models.IntegerField(default=0,
                                        help_text='Cost to paint a Kitchen')
    ceiling_cost = models.IntegerField(default=0,
                                        help_text='Cost to paint a standard '
                                                  'room ceiling')
    stairway_cost = models.IntegerField(default=0,
                                        help_text='Cost to paint a '
                                                  'stairway')
    other_price = models.IntegerField(default=0,
                                        help_text='Cost to paint: Hallway, Closet, '
                                                  ', etc')

    ceiling_trim_cost = models.IntegerField(default=0,
                                             help_text='Cost to paint ceiling '
                                                       'trim for a standard room')

    baseboard_trim_cost = models.IntegerField(default=0,
                                              help_text='Cost to paint baseboard '
                                                        'trim for a standard room')
    

class PaintEstimateUser(models.Model):

    # Model for customers   

    #def __str__(self):              
    #    return self.user_name

    city = models.CharField(default='Toronto', max_length=200)
    bedrooms = models.IntegerField(default=0)
    master_bedroom = models.BooleanField(default=False)
    bathrooms = models.IntegerField(default=0)
    master_bathroom = models.BooleanField(default=False)
    living_room = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)
    ceiling = models.BooleanField(default=False)
    ceiling_height = models.IntegerField(default=0)
    ceiling_trim = models.BooleanField(default=False)
    baseboard_trim = models.BooleanField(default=False)
    other_rooms = models.IntegerField(default=0)
    stairways = models.IntegerField(default=0)
    estimate_cost =  models.IntegerField(default=0)
    email= models.CharField(default=' ', max_length=200)
    name= models.CharField(default=' ', max_length=200)
    phone = models.CharField(default=' ', max_length=200)
    estimate_date = models.DateField()
