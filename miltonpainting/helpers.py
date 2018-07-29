from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
import threading

class EmailThread(threading.Thread):

    def __init__(self, subject, body, from_email, recipient_list, fail_silently, html=None, image=None):
        self.subject = subject
        self.body = body
        self.recipient_list = recipient_list
        self.from_email = from_email
        self.fail_silently = fail_silently
        self.html = html
        self.image = image
        threading.Thread.__init__(self)

    def run (self):
        msg = EmailMultiAlternatives(self.subject, self.body, self.from_email, [self.recipient_list])
        if self.html:
            msg.attach_alternative(self.html, "text/html")
        msg.mixed_subtype = 'related'
        if self.image:
            fp = open(settings.MEDIA_ROOT + '/' + str(self.image), "rb")
            msg_img = MIMEImage(fp.read())
            fp.close()
            image_name = str(self.image).split('/')[-1]
            msg_img.add_header('Content-ID', '<{}>'.format(image_name))
            msg.attach(msg_img)
        msg.send(self.fail_silently)
        
        
def cleanPaintValues(form):

     cleaned_values = {}
     cleaned_values['bedrooms'] = form.cleaned_data['bedrooms']
     cleaned_values['master_bedroom'] = form.cleaned_data['master_bedroom']
     cleaned_values['bathrooms'] = form.cleaned_data['bathrooms']
     cleaned_values['master_bathroom'] = form.cleaned_data['master_bathroom']
     cleaned_values['living_room'] = form.cleaned_data['living_room']
     cleaned_values['kitchen'] = form.cleaned_data['kitchen']
     cleaned_values['ceiling_height'] = form.cleaned_data['ceiling_height']
     cleaned_values['ceiling_painted'] = form.cleaned_data['ceiling_painted']
     cleaned_values['ceiling_trim'] = form.cleaned_data['ceiling_trim']
     cleaned_values['baseboard_trim'] = form.cleaned_data['baseboard_trim']
     cleaned_values['stairways'] = form.cleaned_data['stairways']
     cleaned_values['email'] = form.cleaned_data['email']
     cleaned_values['name'] = form.cleaned_data['name'].replace(" ", "")
     cleaned_values['phone'] = form.cleaned_data['phone']
     cleaned_values['other_rooms'] = form.cleaned_data['other_rooms']
     return cleaned_values
 
 
 # Get the price of the paint estimate
def calculatePaintEstimatePrice(values, estimatePrices):

    standard_ceiling = 8
    # Get the Bedroom cost
    bedroom_cost = 0
    
    if values['master_bedroom']:
        bedroom_cost += estimatePrices.master_bedroom_price
        if int(values['bedrooms']) > 0:
            bedroom_cost +=  estimatePrices.bedroom_price * (values['bedrooms']-1)
    else:
        bedroom_cost += estimatePrices.bedroom_price * values['bedrooms']

    # Get the Bathroom cost
    bathroom_cost = 0
    
    if values['master_bathroom']:
        bathroom_cost += estimatePrices.master_bathroom_price
        if int(values['bathrooms']) > 0:
            bathroom_cost += estimatePrices.bathroom_price * (values['bathrooms']-1)
    else:
        bathroom_cost += estimatePrices.bathroom_price * values['bathrooms']

    # Get the Living Room cost
    living_room_cost = 0
    if values['living_room']:
        living_room_cost = estimatePrices.living_room_price

    # Get the Kitchen cost
    kitchen_cost = 0
    if values['kitchen']:
        kitchen_cost = estimatePrices.kitchen_price

    # Get the Other Rooms cost
    other_cost = values['other_rooms'] * estimatePrices.other_price

    # Get the Other Rooms cost
    stairway_cost = values['stairways'] * estimatePrices.stairway_cost

    # Calculate the estimate cost
    estimate_cost = (int)((bedroom_cost + bathroom_cost + living_room_cost + 
                      kitchen_cost + other_cost + stairway_cost) * (values['ceiling_height'] / float(standard_ceiling)))

    # Add cost of ceiling if it is to be painted
    ceiling_cost = 0
    if values['ceiling_painted'] and estimatePrices.bedroom_price > 0:
        ceiling_cost = int(estimate_cost * (estimatePrices.ceiling_cost / float(estimatePrices.bedroom_price)))
        ceiling_cost = ceiling_cost * (values['ceiling_height'] / float(standard_ceiling))

    # Add cost of ceiling trim for all rooms
    ceiling_trim_cost = 0
    if values['ceiling_trim'] and estimatePrices.bedroom_price > 0:
        ceiling_trim_cost = int(estimate_cost * (estimatePrices.ceiling_trim_cost / float(estimatePrices.bedroom_price)))
        ceiling_trim_cost = ceiling_trim_cost * (values['ceiling_height'] / float(standard_ceiling))

    # Add cost of baseboard trim for all rooms
    baseboard_trim_cost = 0
    if values['baseboard_trim'] and estimatePrices.bedroom_price > 0:
        baseboard_trim_cost = int(estimate_cost * (estimatePrices.baseboard_trim_cost / float(estimatePrices.bedroom_price)))

    estimate_cost += ceiling_cost + ceiling_trim_cost + baseboard_trim_cost
    
    return estimate_cost

# Send an email containing estimate details to the user and the company owner
def sendEmail(estimate, estimate_company):

    estimate_subject = ''
    estimate_details = ''
    estimate_details_html = ''
    message = ''
    message_html = ''
    customer_message = ''
    customer_message_html = ''
    estimate_customer_footer = ''
    estimate_customer_footer_html = ''
    email = ''
    name = ''
    phone = ''
    city = ''
    image = ''
    phone_company = ''
    email_company = ''
    company_name = ''

    # send an email to the client with their requested estimate(s)
    if not estimate_subject:
        estimate_subject = 'Your Paint Estimate Summary - ' + estimate.name
        name = estimate.name
        phone = estimate.phone
        customer_message += 'Dear ' + name + ','
        customer_message += '\n\n Thank you for submitting your estimate.  \n' \
              ' All prep and labour costs are included in the estimate price.  \n' \
              ' The Cost of Paint and any applicable taxes are not included in \n' \
              ' the estimate.  Excessive damage and custom paintwork may adjust \n' \
              ' your estimate price.'
        customer_message += ' \n\n Estimate Details:'
        customer_message_html += 'Dear ' + name + ','
        customer_message_html += ' <br><br><p>Thank you for submitting your estimate. <br>' \
            ' All prep and labour costs are included in the estimate price.  <br>' \
            ' The Cost of Paint and any applicable taxes are not included <br> ' \
            ' in estimate price. Excessive damage and custom paintwork may <br>' \
            ' adjust your estimate price.</p>'
        customer_message_html += ' <br><br><h3><strong>Estimate Details:</strong></h3>'

    if not estimate_details:
        email = estimate.email
        estimate_details += '\n Your Job Details: \n'
        estimate_details_html += '<br><h3><strong>Your Job Details:</strong></h3>'
        estimate_details += '\n Bedrooms: ' + str(estimate.bedrooms)
        estimate_details_html += '<br><strong>Bedrooms:</strong> ' + str(estimate.bedrooms)
        estimate_details += '\n Master Bedroom: '
        if estimate.master_bedroom:
            estimate_details += 'Yes'
        else:
            estimate_details += 'No'
            
        estimate_details += '\n Bathrooms: ' + str(estimate.bathrooms)
        estimate_details_html += ' <br><strong>Bathrooms:</strong> ' + str(estimate.bathrooms)
        
        estimate_details += '\n Master Bathroom: '
        if estimate.master_bathroom:
            estimate_details += 'Yes'
        else:
            estimate_details += 'No'

        estimate_details += '\n Kitchen: '
        estimate_details_html += '<br><strong>Kitchen:</strong> '
        if estimate.kitchen:
            estimate_details += 'Yes'
            estimate_details_html += 'Yes'
        else:
            estimate_details += 'No'
            estimate_details_html += 'No'

        estimate_details += '\n Living Room: '
        estimate_details_html += '<br><strong>Living Room:</strong> '
        if estimate.living_room:
            estimate_details += 'Yes'
            estimate_details_html += 'Yes'
        else:
            estimate_details += 'No'
            estimate_details_html += 'No'

        estimate_details += '\n Stairways: ' + str(estimate.stairways)
        estimate_details_html += '<br><strong>Stairways:</strong> ' + str(estimate.stairways)

        estimate_details += '\n Other Rooms: ' + str(estimate.other_rooms)
        estimate_details_html += '<br><strong>Other Rooms:</strong> ' + str(estimate.other_rooms)

        estimate_details += '\n Ceiling Painted: '
        estimate_details_html += '<br><strong>Ceiling Painted:</strong> '
        if estimate.ceiling:
            estimate_details += 'Yes'
            estimate_details_html += 'Yes'
        else:
            estimate_details += 'No'
            estimate_details_html += 'No'

        estimate_details += '\n Ceiling Height: ' + str(estimate.ceiling_height)
        estimate_details_html += '<br><strong>Ceiling Height:</strong> ' + str(estimate.ceiling_height)

        estimate_details += '\n Ceiling Trim Painted: '
        estimate_details_html += '<br><strong>Ceiling Trim Painted:</strong> '
        if estimate.ceiling_trim:
            estimate_details += 'Yes'
            estimate_details_html += 'Yes'
        else:
            estimate_details += 'No'
            estimate_details_html += 'No'

        estimate_details += '\n Baseboard Trim Painted: '
        estimate_details_html += '<br><strong>Baseboard Trim Painted:</strong> '
        if estimate.baseboard_trim:
            estimate_details += 'Yes'
            estimate_details_html += 'Yes'
        else:
            estimate_details += 'No'
            estimate_details_html += 'No'

        message += '\n Estimate Cost: $' + \
                    str(estimate.estimate_cost)
        message_html += '<br><strong>Estimate Cost:</strong> $' + \
                        str(estimate.estimate_cost)

    estimate_message_footer = '\n \n Thank You For Choosing Fluid Estimates!'
    estimate_message_footer_html = '<br><br> <a href="fluidestimates.com"> <strong> ' \
                                   'Thank you for choosing Fluid Estimates! </strong></a>'
    estimate_message_footer += '\n Email: ' + str(estimate_company.email)
    estimate_message_footer_html += ' <br><strong>Email:<strong> ' + estimate_company.email
    smtp_email = 'bmisljen@gmail.com'

    html_content = customer_message_html + message_html + estimate_details_html + estimate_customer_footer_html + estimate_message_footer_html
    text_content = customer_message + message + estimate_details + estimate_customer_footer + estimate_message_footer
    EmailThread(estimate_subject, text_content, smtp_email,
                email, fail_silently=True, html=html_content).start()

    # Send an email out to us to let us
    # know that the estimate has been done
    estimate_subject = 'New Paint Estimate From - ' + name
    contact_details = ' Contact Details: \n'
    contact_details_html = ' <h3><strong>Contact Details:<strong></h3><br>'
    contact_details += ' Name: ' + name
    contact_details_html += ' <strong>Name:</strong> ' + name
    contact_details += '\n Phone: ' + phone
    contact_details_html += ' <br><strong>Phone:</strong> ' + phone
    contact_details += '\n Email: ' + email + '\n'
    contact_details_html += ' <br><strong>Email:</strong> ' + email
    contact_details += '\n City: ' + city + '\n'
    contact_details_html += ' <br><strong>City:</strong> ' + city + '<br>'

    if estimate_company.email:
        html_content = contact_details_html + message_html + estimate_details_html + estimate_message_footer_html
        text_content = contact_details + message + estimate_details + estimate_message_footer
        EmailThread(estimate_subject, text_content, smtp_email,
                estimate_company.email, fail_silently=True, html=html_content, image=image).start()
