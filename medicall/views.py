import requests
import json

from django.http import HttpResponse
from medicall.credentials import LipanaMpesaPpassword, MpesaAccessToken



from django.shortcuts import render, redirect, get_object_or_404
from .models import Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')
@login_required(login_url='accounts:login')
def appointment(request):
    """ Appointment booking """
    if request.method == 'POST':
        # Create variable to pick the input fields
        appointment = Appointment(
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            date=request.POST['date'],
            department=request.POST['department'],
            doctor=request.POST['doctor'],
            message=request.POST['message'],
        )
        # Save the variable
        appointment.save()
        # Redirect to a page after saving
        return redirect('medicall:index')  # Adjust the redirect to your desired page
    else:
        return render(request, 'appointment.html')

# retrive all appointments
def retrieve_appointments(request):

  appointments = Appointment.objects.all()
  context = {'appointments':appointments}
  return render(request,'show_appointments.html',context)

#delete
def delete_appointment(request, id):
    #deleting 
    appointment = Appointment.objects.get(id=id)
    appointment.delete()
    return redirect("medicall:show_appointments")


#update

def update_appointment(request, id):
    # Retrieve the appointment by its id
    appointment = get_object_or_404(Appointment, id=id)

    # Your form handling or update logic here
    # Example: Update appointment details or return a form

    return render(request, 'medicall/update_appointment.html', {'appointment': appointment})
# @login_required
def upload_image(request):

    # Restrict to superusers only
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to upload images.")

    if request.method == 'POST':
        # Retrieve data from the form
        title = request.POST.get('title')
        uploaded_file = request.FILES.get('image')

        if title and uploaded_file:
            # Save the file using FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_url = fs.url(filename)

            # Save file information to the database
            image = UploadedImage.objects.create(title=title, image=filename)
            image.save()

            return render(request, 'upload_success.html', {'file_url': file_url})
        else:
            return render(request, 'upload_image.html', {'error': 'Please provide both a title and an image.'})

    return render(request, 'upload_image.html')



# Adding the mpesa functions

#Display the payment form
def pay(request):
   """ Renders the form to pay """
   return render(request, 'pay.html')


# Generate the ID of the transaction
def token(request):
    """ Generates the ID of the transaction """
    consumer_key = 'FSacRpfstc5zvmrceKdqCn0kWI9iPyhz5PaltAhtIkNsjyCh'
    consumer_secret = 'Hd4RjLVlFYEf70wqpOMrAW3eBj6Ufx7M08mn1TES8WsWezCBZ6X5XIAELmAxEpOJ'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})


# Send the stk push
def stk(request):
    """ Sends the stk push prompt """
    if request.method =="POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "eMobilis",
            "TransactionDesc": "Web Development Charges"
        }
        response = requests.post(api_url, json=request, headers=headers)
        return HttpResponse("Success")