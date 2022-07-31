""" The docstrings were only generetad to be in accordance to pylint. Its importance is known
but it is no the focus on this moment and will be refactored in the future"""

# TODO: REFACTOR DOCSTRINGS FROM THE WHOLE PROJECT

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import FormContact


def login(request):
    """login"""
    if request.method != "POST":
        return render(request, "account/login.html")

    user = request.POST.get("user")
    password = request.POST.get("password")

    user = auth.authenticate(request, username=user, password=password)

    if not user:
        messages.error(request, "User and/or password not valid!")
        return render(request, "account/login.html")
    else:
        auth.login(request, user)
        messages.success(request, "You have successfully logged in!")
        return redirect("dashboard")


def logout(request):
    """logout"""
    auth.logout(request)
    return redirect('login')


def register(request):
    """register"""
    if request.method != "POST":
        return render(request, "account/register.html")

    fields = ["name", "surname", "email", "user", "password", "password2"]
    fields_values = {}

    for field in fields:
        fields_values[field] = request.POST.get((field))
        if not fields_values[field]:
            messages.error(request, "All values must be filled")
            return render(request, "account/register.html")

    # TODO: Implement Tests and add more validations
    print(fields_values["name"])
    try:
        validate_email(fields_values["email"])

    except ValidationError:
        messages.error(request, "The entered emails is not valid,")
        return render(request, "account/register.html")

    if len(fields_values["password"]) < 6:
        messages.error(request, "The password has to contain at least 6 digits")
        return render(request, "account/register.html")

    if User.objects.filter(username=fields_values["user"]).exists():
        messages.error(request, "The user already exists")
        return render(request, "account/register.html")

    if User.objects.filter(email=fields_values["email"]).exists():
        messages.error(request, "The emai has already being used ")
        return render(request, "account/register.html")

    if fields_values["password"] != fields_values["password2"]:
        messages.error(request, "The passwords must match")
        return render(request, "account/register.html")

    messages.success(request, 'Successfully registered"  Please login in you account.')
    user = User.objects.create_user(
        username=fields_values["user"],
        email=fields_values["email"],
        password=fields_values["password"],
        first_name=fields_values["name"],
        last_name=fields_values["surname"],
    )

    user.save()
    return redirect("login")


@login_required(redirect_field_name="login")
def dashboard(request):
    """dashboards"""
    if request.method != 'POST':
        form = FormContact()
        return render(request, "account/dashboard.html", {'form': form})

    form = FormContact(request.POST, request.FILES)
    
    if not form.is_valid():
        messages.error(request,' Error when sending the data ' )
        form = FormContact(request.POST)
        return render(request, "account/dashboard.html", {'form': form})
    
    form.save()
    return redirect('dashboard')
    
    