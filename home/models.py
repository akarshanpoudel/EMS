from django.db import models
from tinymce.models import HTMLField
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
class Event(models.Model):
    name = models.CharField(max_length=100)
    description = HTMLField()
    dnt = models.DateTimeField()
    venue = models.CharField(max_length=50)
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    # Indented correctly inside the class, removed the clashing database field
    @property
    def seats(self):
        total = self.total_seats
        # Fixed typos: changed .booking to .bookings and .coutn() to .count()
        taken = self.bookings.all().count()
        return total - taken

    def __str__(self):
        return self.name


class Bookings(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookings")
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Booking"
        verbose_name_plural = "Bookings"
        
    # Moved out of class Meta into the main Bookings class level
    def __str__(self):
        username = self.participant.username if self.participant else "Unknown"
        event_name = self.event.name if self.event else "Unknown Event"
        return f"{username} - {event_name}"
        

# Un-nested from Bookings so it functions as a proper root-level proxy model
class ExpireEvent(Event):
    class Meta:
        proxy = True
        verbose_name = "Expired Event"
        verbose_name_plural = "Expired Events"