from django.db import models

class MasterData(models.Model):
    work_start = models.TimeField()
    work_end = models.TimeField()
    slot_minutes = models.IntegerField()
    capacity_per_slot = models.IntegerField()

    def __str__(self):
        return "Master Data"

class Slot(models.Model):
    slot_date = models.DateField()
    slot_time = models.TimeField()

    class Meta:
        unique_together = ('slot_date', 'slot_time')

    def __str__(self):
        return f"{self.slot_date} {self.slot_time}"

class Booking(models.Model):
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE, related_name="bookings")
    truck_plate = models.CharField(max_length=20)
    customers = models.IntegerField()
    operation_type = models.CharField(max_length=20)  # Loading / Unloading
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.truck_plate} @ {self.slot}"

