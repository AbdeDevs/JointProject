from datetime import datetime

from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from Guest import utils
from Guest.config import Config as c
from Guest.forms import RestaurantReservationForm, SearchClientForm
from Reception.forms import RoomReservationForm
from Reception.models import RoomReservation, create_despesa, Room, Client
from Restaurant.forms import CreateExternalClientForm
from Restaurant.models import RestaurantReservation, ExternalRestaurantClient


def guest_home(request):
    return render(request, c.get_guest_home_path())


def guest_room_reservation_1(request):
    """Client creates a new reservation."""
    if request.method == 'POST':
        form = RoomReservationForm(request.POST)
        """Get the first available room of the chosen type."""
        try:
            room = Room.objects.filter(room_type=request.POST.get('room_type'), is_taken=False).first()
        except Room.DoesNotExist:
            messages.error(request, "No hi ha habitacions d'aquest tipus disponibles")
            room = None

        """Get the client based on the current user session."""
        try:
            client = Client.objects.get(id=request.user.id)
        except Client.DoesNotExist:
            messages.error(request, "Error al rebre les dades del client. Torna-ho a intentar")
            client = None

        if room and client:
            entry_date = datetime.strptime(request.POST.get('entry'), '%d/%m/%Y').strftime('%Y-%m-%d')
            exit_date = datetime.strptime(request.POST.get('exit'), '%d/%m/%Y').strftime('%Y-%m-%d')
            new_rsv = RoomReservation(
                client=client,
                room=room,
                entry=entry_date,
                exit=exit_date,
                pension_type=request.POST.get('pension_type'),
                num_guests=request.POST.get('num_guests')
            )
            room.is_taken = True
            room.save()
            new_rsv.save()
            create_despesa(new_rsv, new_rsv.pension_type, room.room_type)
            return redirect(c.get_guest_home_path())
    else:
        form = RoomReservationForm()

    return render(request, c.get_guest_path(1), {'form': form})


def guest_restaurant_reservation_1(request):
    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            reservation_data = form.cleaned_data
            reservation_data['day'] = reservation_data['day'].strftime('%Y-%m-%d')
            request.session['reservation_data'] = reservation_data
            return redirect('guest_restaurant_reservation_2')
    else:
        form = RestaurantReservationForm()
    return render(request, c.get_guest_path(2), {'form': form})


def guest_restaurant_reservation_2(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('guest_restaurant_reservation_1')

    if request.method == 'POST':
        form = SearchClientForm(request.POST)

        if form.is_valid():
            client_type = utils.get_client_type(form.cleaned_data['id_number'])
            if client_type == 'internal':
                reservation_data['id_number'] = form.cleaned_data['id_number']
                request.session['reservation_data'] = reservation_data
                return redirect('guest_restaurant_reservation_3')
            elif client_type == 'external':
                return redirect('guest_restaurant_reservation_4')

    else:
        form = SearchClientForm()
    return render(request, c.get_guest_path(3), {'form': form})


def guest_restaurant_reservation_3(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('guest_restaurant_reservation_1')

    if request.method == 'POST':
        reservation_action = request.POST.get('reservation_action')
        if reservation_action == 'Confirmar Reserva':
            utils.create_restaurant_reservation(reservation_data)
            del request.session['reservation_data']
            messages.success(request, "S'ha creat la reserva de restaurant amb èxit!")
            return redirect('guest_home')
        elif reservation_action == 'Cancelar Reserva':
            del request.session['reservation_data']
            messages.success(request, "S'ha cancelat el proces de reserva de restaurant!")

            return redirect('guest_home')

    return render(request, c.get_guest_path(4))


def guest_restaurant_reservation_4(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('guest_restaurant_reservation_1')

    if request.method == 'POST':
        ClientForm = modelform_factory(ExternalRestaurantClient, form=CreateExternalClientForm)
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            external_client = form.save()
            reservation = RestaurantReservation(
                client=None,
                external_client=external_client,
                day=datetime.strptime(reservation_data['day'], '%Y-%m-%d').date(),
                num_guests=reservation_data['num_guests'],
                service=reservation_data['service'],
                is_active=True
            )
            reservation.save()
            del request.session['reservation_data']
            messages.success(request, "S'ha creat la reserva de restaurant amb èxit!")
            return redirect('guest_home')
    form = modelform_factory(ExternalRestaurantClient, form=CreateExternalClientForm)
    return render(request, c.get_guest_path(5), {'form': form})
