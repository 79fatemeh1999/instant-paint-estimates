from .models import PaintEstimate
from django import forms
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.utils.safestring import mark_safe
from datetime import datetime

class PaintEstimateForm(forms.Form):

    TRUE_FALSE_CHOICES = (
        (True, 'Yes'),
        (False, 'No')
    )
    
    city = forms.CharField(label='City',
                           initial='Toronto',
                           required=True,
                           help_text='The city that you live in')
    
    bedrooms = forms.IntegerField(initial=0,
                                  label='Total Bedrooms',
                                  min_value=0,
                                  help_text='Total Number of Bedrooms to be'
                                            ' Painted')

    master_bedroom = forms.ChoiceField(choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       widget=forms.Select(), 
                                       help_text='Is one of the Bedrooms a '
                                                  'Master Bedroom?')

    bathrooms = forms.IntegerField(initial=0,
                                   label='Total Bathrooms',
                                   min_value=0,
                                   help_text='Total Number of Bedrooms to '
                                             'be Painted')

    master_bathroom = forms.ChoiceField(label='Master Bathroom',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Is one of the Bathrooms a '
                                                  'Master Bathroom?',
                                       widget=forms.Select())
    
    living_room = forms.ChoiceField(label='Living Room',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Living room painted?',
                                       widget=forms.Select())

    kitchen = forms.ChoiceField(label='Kitchen',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Kitchen painted?',
                                       widget=forms.Select())

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

    ceiling_painted = forms.ChoiceField(label='Ceiling',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Ceiling painted?',
                                       widget=forms.Select())

    ceiling_trim = forms.ChoiceField(label='Ceiling Trim',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Ceiling trim painted?',
                                       widget=forms.Select())

    baseboard_trim = forms.ChoiceField(label='Baseboard Trim',
                                       choices = TRUE_FALSE_CHOICES,
                                       required=True,
                                       initial=False,
                                       help_text='Baseboard trim painted?',
                                       widget=forms.Select())

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
    
    estimate_date = forms.DateField(label='Date for Estimate',
                                    help_text='Date for in person estimate',
                                    required=True)


    def __init__(self, *args, **kwargs):
        super(PaintEstimateForm, self).__init__(*args, **kwargs)
        
        dateTimeOptions = {
            'format': 'dd/mm/yyyy',
            'autoclose': True,
            'showMeridian': True,
            'todayHighlight': True,
        }
        self.fields['estimate_date'].widget = DateWidget(options=dateTimeOptions, usel10n = True, bootstrap_version=4, attrs={'id':"estimate_date"})

        for field in self.fields:
            self.fields[field].help_text = mark_safe("<small class='form-text text-muted'>" + self.fields[field].help_text + "</small>")
            

    def clean_estimate_date(self):
        estimate_date = self.cleaned_data.get('estimate_date', False)
        if estimate_date:
            date_current = datetime.now().date()
            if estimate_date < date_current:
                raise ValidationError("Cannot book an appointment in the past")
            return estimate_date
        else:
            return estimate_date