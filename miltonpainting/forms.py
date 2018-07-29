from .models import PaintEstimate
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class PaintEstimateForm(forms.Form):

    bedrooms = forms.IntegerField(initial=0,
                                  label='Total Bedrooms',
                                  min_value=0,
                                  help_text='Total Number of Bedrooms to be'
                                            ' Painted')

    master_bedroom = forms.BooleanField(label='Master Bedroom',
                                        required=False,
                                        initial=False,
                                        help_text='Is one of the Bedrooms a '
                                                  'Master Bedroom?')

    bathrooms = forms.IntegerField(initial=0,
                                   label='Total Bathrooms',
                                   min_value=0,
                                   help_text='Total Number of Bedrooms to '
                                             'be Painted')

    master_bathroom = forms.BooleanField(label='Master Bathroom',
                                        required=False,
                                        initial=False,
                                        help_text='Is one of the Bathrooms a'
                                                  ' Master Bathroom?')

    living_room = forms.BooleanField(label='Living Room',
                                     required=False,
                                     initial=False,
                                     help_text='Living Room Painted?')

    kitchen = forms.BooleanField(label='Kitchen',
                                 required=False,
                                 initial=False,
                                 help_text='Kitchen Painted?')

    stairways = forms.IntegerField(label='Stairway',
                                  required=False,
                                  initial=0,
                                  min_value=0,
                                  help_text='Number of Stairways to be Painted')

    other_rooms = forms.IntegerField(label='Other Rooms',
                                     required=False,
                                     initial=0,
                                     min_value=0,
                                     help_text='Includes Hallway, Closet, '
                                               'etc.')

    ceiling_height = forms.IntegerField(label='Ceiling Height',
                                        required=True,
                                        initial=8,
                                        max_value=25,
                                        min_value=8,
                                        help_text='Ceiling Height in Feet for '
                                                  'all rooms')

    ceiling_painted = forms.BooleanField(label='Ceiling Painted',
                                      required=False,
                                      initial=False,
                                      help_text='Ceiling Painted for all rooms')

    ceiling_trim = forms.BooleanField(label='Ceiling Trim',
                                      required=False,
                                      initial=False,
                                      help_text='Ceiling Trim or Crown Moulding '
                                                'Painted for all rooms')

    baseboard_trim = forms.BooleanField(label='Baseboard Trim',
                                        required=False,
                                        initial=False,
                                        help_text='Baseboard Trim Painted for '
                                                  'all rooms')

    email = forms.CharField(label='Email',
                            required=True,
                            validators=[
                            RegexValidator(
                            regex='[^@]+@[^@]+\.[^@]+',
                            message='Email must have @',
                            ),
                            ],
                            help_text='Your Email ex. john.smith@gmail.com')

    name = forms.CharField(label='Name',
                            required=True,
                            help_text='Your Name ex. John Smith')

    phone = forms.CharField(label='Phone', required=True,
                            validators=[
                            RegexValidator(
                            regex='^[\dA-Z]{3}-?[\dA-Z]{3}-?[\dA-Z]{4}$',
                            message='Phone must have 10 digits',
                            ),
                            ],
                            help_text='ex. 123-456-7890')

    def __init__(self, *args, **kwargs):
        super(PaintEstimateForm, self).__init__(*args, **kwargs)
      

