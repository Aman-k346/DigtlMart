from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from main.phonepay_client import create_payment
import json
import base64




phonepe_client = PhonePePaymentClient(merchant_id=settings.PHONEPE_MERCHANT_ID, salt_key=settings.PHONEPE_MERCHANT_KEY, salt_index=1, env=Env.PROD, should_publish_events=True)

# Create your views here.

def home(request):
    return render(request, 'home.html')

def terms(request):
    return render(request, 'terms.html')

def VideoBundle(request):
    if request.user.is_authenticated:
        userid = request.user.id
        try:
            payment = Payment.objects.get(user_id=userid)
            if payment.status == 'COMPLETED':
                download_link = "https://your-download-link.com/resource"  
                context = {
                    'status': 'COMPLETED',
                    'download_link': download_link 
                }
                return render(request, 'videobundle.html', context=context)
        except Payment.DoesNotExist:
            pass

    return render(request, 'videobundle.html')


def refund(request):
    return render(request, 'refund.html')

def privacy(request):
    return render(request, 'privacy.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # Log the user in
            auth_login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('/')  # Redirect to home or dashboard after successful login
        else:
            # If authentication fails
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if not email.endswith('@gmail.com'):
            messages.error(request, 'Only gmail emails are accepted.')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'register.html')

        user = User.objects.create(
            username=email,  
            email=email,
            password=make_password(password) 
        )
        user.save()

        messages.success(request, 'Email registered successfully. Please log in.')

    return render(request, 'register.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('/') 

def checkout(request):
    return render(request, 'checkout.html')


@csrf_exempt
def initiate_payment(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    if request.method == 'POST':
        amount = 149 * 100  # Amount in paisa

        try:
            userid = request.user.id
            
            # Check if the user already has a completed payment
            existing_payment = Payment.objects.filter(user_id=userid, status='COMPLETED').first()
            if existing_payment:
                return redirect('/bundle?already_bought=true')
            
            # Check if there is a pending payment
            pending_payment = Payment.objects.filter(user_id=userid, status='PENDING').first()
            if pending_payment:
                pay_page_url = create_payment(amount, userid) 
                pending_payment.merchant_transaction_id = pay_page_url[1] 
                pending_payment.save()  

                return redirect(pay_page_url[0])

            # Proceed to create a new payment and get the redirect URL
            pay_page_url, merchant_transaction_id = create_payment(amount, userid)
            Payment.objects.create(
                user_id=userid,
                amount=amount,
                status='PENDING',
                merchant_transaction_id=merchant_transaction_id,
            )

            return redirect(pay_page_url)

        except Exception as e:
            return redirect('checkout')
        

@csrf_exempt
def payment_callback(request):
   
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            x_verify_header_data = request.headers.get("X-VERIFY")

            body_data = json.loads(body)
            encoded_response = body_data.get('response')
            decoded_response = base64.b64decode(encoded_response).decode('utf-8')

            # Parse the decoded response to get payment details
            response_data = json.loads(decoded_response)
            status = response_data.get('data', {}).get('state')
            transaction_id = response_data.get('data', {}).get('transactionId')
            merchant_TransactionId = response_data.get('data', {}).get('merchantTransactionId')

            amount = response_data.get('data', {}).get('amount', 0) / 100.0  # Convert from paisa to INR

            # Create or update the payment entry based on merchantTransactionId
            payment, created = Payment.objects.get_or_create(
                merchant_transaction_id=merchant_TransactionId,
                defaults={
                    'amount': amount,
                    'status': 'PENDING',  # Initially set to PENDING
                    'transaction_id': transaction_id
                }
            )

            if status == 'COMPLETED':
                payment.status = 'COMPLETED'  # Update status to COMPLETED
                payment.amount = amount
                payment.transaction_id = transaction_id
                payment.save()
                
                return redirect('/success') 

            else:
                reason = response_data.get('data', {}).get('reason', 'Payment failed due to unknown reasons.')
                return redirect(f'/failed?reason={reason}')  

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    elif request.method == 'GET':
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)

    return JsonResponse({"status": "error", "message": "Unsupported request method"}, status=405)


def success_page(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    
    userid = request.user.id  

    try:
        payment = Payment.objects.get(user_id=userid) 

        if payment.status != 'COMPLETED':
            reason = "Something went wrong."
            return redirect(f'/failed?reason={reason}') 
        
        context = {
            'amount': payment.amount,
            'message': 'Payment was successful! Thank you for your purchase.'
        }
        return render(request, 'success.html', context)
    
    except Payment.DoesNotExist:
        reason = "Something went wrong."
        return redirect(f'/failed?reason={reason}')
    except Exception as e:
        return redirect(f'/failed?reason={str(e)}') 


def failed_page(request):
    
    reason = request.GET.get('reason', 'Something went wrong.')
    context = {'reason': reason} 
    return render(request, 'failed.html', context)
