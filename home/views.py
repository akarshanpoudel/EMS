from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse  
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied
from .forms import EventForm
from .models import Event, Bookings
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

# === AUTHENTICATION VIEWS ===

def register_view(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


# === EVENT MANAGEMENT VIEWS ===

def home(request):

    current_time = timezone.now()
    
    upcoming_events = Event.objects.filter(date__gte=current_time).order_by('date')
    
    context = {
        'events': upcoming_events
    }
    return render(request, 'home.html', context)

def create_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            # Automatically assign the logged-in user as the organizer if needed
            event = form.save(commit=False)
            if request.user.is_authenticated:
                event.organizer = request.user
            event.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'event_form.html', context)


@login_required
def edit_event(request, event_id):
    # Fetch the event securely or return a 404
    event = get_object_or_404(Event, id=event_id)
    
    # SECURITY: Prevent non-organizers from tinkering with this event
    if event.organizer != request.user:
        raise PermissionDenied("You do not have permission to edit this event.")
        
    if request.method == 'POST':
        # Passing 'instance=event' tells Django to UPDATE this row rather than creating a new one
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        # Pre-populate the form fields with the current event details
        form = EventForm(instance=event)
        
    context = {
        'form': form,
        'event': event,
        'is_edit': True  # Useful flag to alter template headings dynamically (e.g., "Edit Event")
    }
    return render(request, 'event_form.html', context)


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    bookings = event.bookings.all().order_by('booked_at')
    
    user_has_joined = False
    my_seat_index = -1
    
    if request.user.is_authenticated:
        for index, booking in enumerate(bookings):
            if booking.participant == request.user:
                user_has_joined = True
                my_seat_index = index
                break
                
    context = {
        'event': event,
        'attendees': bookings,
        'user_has_joined': user_has_joined,
        'my_seat_index': my_seat_index,
        'seat_range': range(event.total_seats),
    }
    return render(request, 'event_detail.html', context)


def join_event(request, event_id):
    event = Event.objects.get(id=event_id)
    next_url = request.GET.get('next', reverse('event_detail', args=[event_id]))
    
    if event.seats > 0:
        Bookings.objects.create(participant=request.user, event=event)
        
        if request.user.email:  
            subject = f"Seat Confirmed: {event.name}"
            message = (
                f"Hi {request.user.username},\n\n"
                f"You have successfully booked a seat for '{event.name}'!\n\n"
                f"Event Details:\n"
                f"Venue: {event.venue}\n"
                f"Date & Time: {event.dnt.strftime('%B %d, %Y at %I:%M %p')}\n\n"
                f"See you there!\n"
                f"- The EventHive Team"
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False, 
            )
            
    return redirect(next_url)


def cancel_seat(request, event_id):
    event = Event.objects.get(id=event_id)
    booking = Bookings.objects.filter(participant=request.user, event=event).first()
    
    if booking:
        if request.user.email:
            subject = f"Booking Cancelled: {event.name}"
            message = (
                f"Hi {request.user.username},\n\n"
                f"This email confirms that your seat reservation for '{event.name}' has been successfully cancelled.\n"
                f"Your slot has been released back to the event organizer.\n\n"
                f"Changed your mind? You can always re-book your ticket on EventHive if open seats are still available.\n\n"
                f"Best regards,\n"
                f"- The EventHive Team"
            )
            
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=False, 
            )
        
        booking.delete()
        
    next_url = request.GET.get('next', reverse('event_detail', args=[event_id]))
    return redirect(next_url)


def my_bookings(request):
    bookings = Bookings.objects.filter(participant=request.user)
    context = {'bookings': bookings}
    return render(request, 'my_bookings.html', context)


def my_events(request):
    events = Event.objects.filter(organizer=request.user)
    context = {'events': events}
    return render(request, 'my_events.html', context)