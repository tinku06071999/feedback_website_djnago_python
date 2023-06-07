from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import Suggestion
from django.contrib import messages
from django.db import IntegrityError
import requests
from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.conf import settings
import random
import hashlib
from django.contrib.auth.hashers import make_password
from .models import PasswordResetToken


# Create your views here.
def index(request):
    return render(request, "index.html")


def signupview(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        try:
            if not last_name:
                raise ValueError("The last name must be set.")

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            return redirect("signup_success")

        except IntegrityError:
            return render(
                request,
                "signup.html",
                {"error_message": "Username is already taken."},
            )
        except ValueError:
            return render(
                request,
                "signup.html",
                {"error_message": "The given username must be set."},
            )

    else:
        return render(request, "signup.html")


def signup_success_view(request):
    return render(request, "login.html")


def Login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("next")
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            return redirect("login")
    else:
        return render(request, "login.html")


def Next(request):
    return render(request, "next.html")


def suggestion_submit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        suggestion_text = request.POST.get("suggestion")

        suggestion = Suggestion(name=name, email=email, suggestion=suggestion_text)
        suggestion.save()

        return redirect("suggestion_success")
    # Redirect to a success page after submission
    messages.success(request, "Your suggestion has been submitted successfully!")
    return render(request, "suggestion.html")


def suggestion_success(request):
    return render(request, "next.html")


def logout(request):
    return render(request, "index.html")


# views.py
def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        # Check if the email exists in the database
        if User.objects.filter(email=email).exists():
            # Generate a random token
            token = hashlib.sha256(str(random.random()).encode("utf-8")).hexdigest()
            # Save the token to the user's database record
            user = User.objects.get(email=email)
            password_reset_token = PasswordResetToken(user=user, token=token)
            password_reset_token.save()
            user.token = token
            user.save()
            # Send the password reset email
            subject = "Password Reset"
            message = f"Hi {user.username},\n\n To reset your password, click the following link:\n\n {request.build_absolute_uri('/reset-password/')}{token}\n\n If you didn't request a password reset, please ignore this email.\n\nThanks,\n The TalentServe Team"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]

            # Sendinblue API configuration
            url = "https://api.sendinblue.com/v3/smtp/email"
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "api-key": settings.SENDINBLUE_API_KEY,
            }
            data = {
                "sender": {"name": "TalentServe", "email": from_email},
                "to": [{"email": email}],
                "subject": subject,
                "htmlContent": message,
            }

            # Send email using Sendinblue API
            try:
                response = requests.post(url, headers=headers, json=data)
                if response.status_code == 201:
                    return render(request, "forgot_password_success.html")
                else:
                    messages.error(request, "Failed to send password reset email.")
            except requests.exceptions.RequestException:
                messages.error(request, "Failed to send password reset email.")
        else:
            messages.error(request, "Entered email does not match any record.")
    return render(request, "forgot_password.html")


def forgot_password_success(request):
    return render(request, "forgot_password_success.html")


# views.py


def recovery_password(request, reset_token):
    if request.method == "POST":
        # Handle the password reset form submission
        # Retrieve the new password from the form
        new_password = request.POST.get("password")

        # Perform the necessary steps to reset the password
        # For example, update the user's password in the database

        try:
            if reset_token:
                token_obj = get_object_or_404(PasswordResetToken, token=reset_token)
                user = token_obj.user
                # Save the user object to update the password and token fields
                user.set_password(new_password)
                user.save()
                token_obj.delete()
                return render(request, "login.html")
            else:
                return render(
                    request,
                    "recovery_password.html",
                    {"error_message": "Invalid reset token."},
                )
        except PasswordResetToken.DoesNotExist:
            return render(
                request,
                "recovery_password.html",
                {"error_message": "Invalid reset token."},
            )

    else:
        # Display the password reset form
        return render(request, "recovery_password.html", {"reset_token": reset_token})
