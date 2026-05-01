from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime
from .models import Slot, Booking, MasterData
from .logic.slot_generator import generate_slots_for_date


def dashboard(request):
    today = datetime.today().date()
    generate_slots_for_date(today)
    slots = Slot.objects.filter(slot_date=today).order_by("slot_time")
    md = MasterData.objects.first()

    capacity = md.capacity_per_slot
    threshold = capacity * 0.7  # <-- add this

    return render(request, "scheduling/dashboard.html", {
        "slots": slots,
        "capacity": capacity,
        "threshold": threshold
    })


def book_slot(request):
    date_str = request.GET.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.today().date()
    generate_slots_for_date(date)
    slots = Slot.objects.filter(slot_date=date).order_by("slot_time")
    md = MasterData.objects.first()

    if request.method == "POST":
        slot_id = request.POST["slot"]
        truck_plate = request.POST["truck_plate"]
        customers = request.POST["customers"]
        operation_type = request.POST["operation_type"]
        notes = request.POST["notes"]

        slot = Slot.objects.get(id=slot_id)
        md = MasterData.objects.first()

        if slot.bookings.count() >= md.capacity_per_slot:
            messages.error(request, "This slot is full.")
        else:
            Booking.objects.create(
                slot=slot,
                truck_plate=truck_plate,
                customers=customers,
                operation_type=operation_type,
                notes=notes
            )
            messages.success(request, "Booking created.")
            return redirect("dashboard")

    return render(request, "scheduling/book_slot.html", {
        "slots": slots,
        "date": date,
        "capacity": md.capacity_per_slot
    })


def schedule_overview(request):
    date_str = request.GET.get("date")
    date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.today().date()
    slots = Slot.objects.filter(slot_date=date).order_by("slot_time")
    return render(request, "scheduling/schedule_overview.html", {
        "slots": slots,
        "date": date
    })


def master_data(request):
    md = MasterData.objects.first()

    if request.method == "POST":
        md.work_start = request.POST["work_start"]
        md.work_end = request.POST["work_end"]
        md.slot_minutes = request.POST["slot_minutes"]
        md.capacity_per_slot = request.POST["capacity_per_slot"]
        md.save()
        messages.success(request, "Master data updated.")

    return render(request, "scheduling/master_data.html", {"md": md})
