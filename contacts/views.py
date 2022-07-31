""" Django - Views.py"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.core.paginator import Paginator
from django.db.models import Q, Value
from django.db.models.functions import Concat
from .models import Contact
from django.contrib import messages


def index(request):
    contacts = Contact.objects.order_by("name").filter(display=True)
    paginator = Paginator(
        contacts, 15
    )  # This content was only choosen due to validation purposes

    page = request.GET.get("p")
    contacts = paginator.get_page(page)
    return render(request, "contacts/index.html", {"contacts": contacts})


def display_contact(request, contact_id):
    contact = get_object_or_404(Contact, id=contact_id)
    if not contact.display:
        raise Http404()
    return render(request, "contacts/display_contact.html", {"contact": contact})


def search(request):
    term = request.GET.get("term")
    fields = Concat("name", Value(" "), "surname")

    if term is None or not term:
        messages.add_message(request, messages.ERROR, "This field cannot be empty")
        return redirect("index")

    # Search by name OR surname but NOT from 'name surname'
    # contacts = Contact.objects.order_by("name").filter(
    #   Q(name__icontains=term) | Q(surname__contains=term), display=True
    # """

    # Search by name, surname or its variations
    contacts = Contact.objects.annotate(complete_name=fields).filter(
        Q(complete_name__icontains=term) | Q(phone__icontains=term), display=True
    )
    paginator = Paginator(
        contacts, 15
    )  # This content was only choosen due to validation purposes
    page = request.GET.get("p")
    contacts = paginator.get_page(page)
    return render(request, "contacts/search.html", {"contacts": contacts})
