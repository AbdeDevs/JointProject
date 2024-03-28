from django.shortcuts import render

from Reception.forms import AddClientForm, RoomReservationForm, RoomForm, InfoClientForm


# Create your views here.
def add_client(request):
    """Add a new client to the database."""
    if request.method == 'POST':
        form = AddClientForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = AddClientForm()
    return render(request, 'reception/add_client.html', {'form': form})


def room_reservation(request):
    """Reserve a room for a client."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RoomReservationForm()
    return render(request, 'reception/room_reservation.html', {'form': form})


def add_room(request):
    """Add a new room to the database."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = RoomForm()
    return render(request, 'reception/add_room.html', {'form': form})


#Check-in views

def check_in(request):
    """Check-in a client."""
    if request.method == 'POST':
        form = InfoClientForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = InfoClientForm()
    return render(request, 'reception/check_in.html', {'form': form})