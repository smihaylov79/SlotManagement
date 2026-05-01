from rest_framework import serializers
from .models import Slot, Booking, MasterData

class SlotSerializer(serializers.ModelSerializer):
    booked = serializers.SerializerMethodField()
    capacity = serializers.SerializerMethodField()

    class Meta:
        model = Slot
        fields = ['id', 'slot_date', 'slot_time', 'booked', 'capacity']

    def get_booked(self, obj):
        return obj.bookings.count()

    def get_capacity(self, obj):
        md = MasterData.objects.first()
        return md.capacity_per_slot

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class MasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterData
        fields = '__all__'
