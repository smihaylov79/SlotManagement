from datetime import datetime, timedelta, time
from scheduling.models import MasterData, Slot

def generate_slots_for_date(date):
    md = MasterData.objects.first()
    if not md:
        raise Exception("MasterData not initialized")

    start = datetime.combine(date, md.work_start)
    end = datetime.combine(date, md.work_end)
    delta = timedelta(minutes=md.slot_minutes)

    current = start
    while current < end:
        Slot.objects.get_or_create(
            slot_date=date,
            slot_time=current.time()
        )
        current += delta
