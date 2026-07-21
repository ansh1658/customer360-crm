from datetime import timedelta
import csv

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommunicationForm
from .models import Communication


def dashboard(request):
    total = Communication.objects.count()

    inbound = Communication.objects.filter(
        direction="Inbound"
    ).count()

    outbound = Communication.objects.filter(
        direction="Outbound"
    ).count()

    last30 = Communication.objects.filter(
        created_at__gte=timezone.now() - timedelta(days=30)
    ).count()

    recent = Communication.objects.order_by("-created_at")[:5]

    context = {
        "total": total,
        "inbound": inbound,
        "outbound": outbound,
        "last30": last30,
        "recent": recent,
    }

    return render(
        request,
        "customer360/dashboard.html",
        context,
    )


def communication_list(request):
    communications = Communication.objects.all().order_by("-created_at")

    query = request.GET.get("q", "")

    if query:
        communications = communications.filter(
            Q(customer_name__icontains=query)
            | Q(email__icontains=query)
            | Q(phone__icontains=query)
            | Q(summary__icontains=query)
        )

    channel = request.GET.get("channel")

    if channel:
        communications = communications.filter(channel=channel)

    direction = request.GET.get("direction")

    if direction:
        communications = communications.filter(direction=direction)

    paginator = Paginator(communications, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    context = {
        "communications": page_obj,
        "page_obj": page_obj,
        "query": query,
        "selected_channel": channel,
        "selected_direction": direction,
    }

    return render(
        request,
        "customer360/communication_list.html",
        context,
    )


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        'attachment; filename="communications.csv"'
    )

    writer = csv.writer(response)

    writer.writerow(
        [
            "Customer",
            "Email",
            "Phone",
            "Channel",
            "Direction",
            "Summary",
            "Created At",
        ]
    )

    communications = Communication.objects.all().order_by("-created_at")

    for communication in communications:
        writer.writerow(
            [
                communication.customer_name,
                communication.email,
                communication.phone,
                communication.channel,
                communication.direction,
                communication.summary,
                communication.created_at.strftime("%d-%m-%Y %H:%M"),
            ]
        )

    return response

def add_communication(request):
    if request.method == "POST":
        form = CommunicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Communication added successfully.")
            return redirect("communication_list")
    else:
        form = CommunicationForm()

    return render(
        request,
        "customer360/communication_form.html",
        {
            "form": form,
            "title": "Add Communication",
        },
    )


def edit_communication(request, pk):
    communication = get_object_or_404(
        Communication,
        pk=pk,
    )

    if request.method == "POST":
        form = CommunicationForm(
            request.POST,
            instance=communication,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Communication updated successfully.")
            return redirect("communication_list")
    else:
        form = CommunicationForm(instance=communication)

    return render(
        request,
        "customer360/communication_form.html",
        {
            "form": form,
            "title": "Edit Communication",
        },
    )


def delete_communication(request, pk):
    communication = get_object_or_404(
        Communication,
        pk=pk,
    )

    if request.method == "POST":
        communication.delete()
        messages.success(request, "Communication deleted successfully.")
        return redirect("communication_list")

    return render(
        request,
        "customer360/communication_confirm_delete.html",
        {
            "communication": communication,
        },
    )


def customer_detail(request, customer_name):
    communications = (
        Communication.objects.filter(
            customer_name=customer_name
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "customer360/customer_detail.html",
        {
            "customer_name": customer_name,
            "communications": communications,
        },
    )