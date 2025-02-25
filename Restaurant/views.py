from datetime import datetime

from django.contrib import messages
from django.forms import modelform_factory
from django.shortcuts import render, redirect

from Restaurant.config import Config as c
from Restaurant.forms import NewRestaurantReservationForm, AddInternalClientForm, CreateExternalClientForm
from Restaurant.models import RestaurantReservation, ExternalRestaurantClient
from Restaurant.utils import get_ordered_reservations
from User.decorators import worker_required


@worker_required('restaurant')
def restaurant_home(request):
    return render(request, c.get_restaurant_home_path())


@worker_required('restaurant')
def new_restaurant_reservation_1(request):
    if request.method == 'POST':
        form = NewRestaurantReservationForm(request.POST)
        if form.is_valid():
            reservation_data = form.cleaned_data
            reservation_data['day'] = reservation_data['day'].strftime('%Y-%m-%d')
            request.session['reservation_data'] = reservation_data
            return redirect('new_restaurant_reservation_2')
    else:
        form = NewRestaurantReservationForm()

    return render(request, c.get_restaurant_new_reservation_path(1), {'form': form})


@worker_required('restaurant')
def new_restaurant_reservation_2(request):
    reservation_data = request.session.get('reservation_data')
    if not reservation_data:
        return redirect('new_restaurant_reservation_1')

    if request.method == 'POST':
        client_type = request.POST.get('client_type')
        if client_type:
            request.session['client_type'] = client_type
            return redirect('new_restaurant_reservation_3')

    return render(request, c.get_restaurant_new_reservation_path(2), {})


@worker_required('restaurant')
def new_restaurant_reservation_3(request):
    reservation_data = request.session.get('reservation_data')
    client_type = request.session.get('client_type')
    if not reservation_data or not client_type:
        return redirect('new_restaurant_reservation_1')

    if client_type == 'internal':
        ClientForm = modelform_factory(RestaurantReservation, form=AddInternalClientForm)
    else:
        ClientForm = modelform_factory(ExternalRestaurantClient, form=CreateExternalClientForm)

    if request.method == 'POST':
        form = ClientForm(request.POST)

        if form.is_valid():
            if client_type == 'internal':
                reservation = form.save(commit=False)
                reservation.client = form.cleaned_data['client']
                reservation.day = datetime.strptime(reservation_data['day'], '%Y-%m-%d').date()
                reservation.num_guests = reservation_data['num_guests']
                reservation.service = reservation_data['service']
                reservation.is_active = True
            else:
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
            return redirect('restaurant_home')
    else:
        form = ClientForm()
    return render(request, c.get_restaurant_new_reservation_path(3), {'form': form})


@worker_required('restaurant')
def restaurant_reservations(request):
    reservations = get_ordered_reservations()
    reservation_details = []

    for reservation in reservations:
        client_id = None
        client_name = "No especificat"
        client_last_name = ""
        is_internal = False
        client_arrvied = reservation.client_arrived

        if reservation.client:
            client = reservation.client
            client_id = client.id
            client_name = client.first_name
            client_last_name = client.last_name
            is_internal = True
        elif reservation.external_client:
            external_client = reservation.external_client
            client_id = external_client.id
            client_name = external_client.first_name
            client_last_name = external_client.last_name
            is_internal = False

        reservation_details.append({
            'reservation_id': reservation.id,
            'client_id': client_id,
            'client_name': client_name,
            'client_last_name': client_last_name,
            'day': reservation.day,
            'num_guests': reservation.num_guests,
            'service': reservation.service,
            'is_active': reservation.is_active,
            'client_arrived': client_arrvied,
            'is_internal': is_internal
        })

    return render(request, c.get_restaurant_check_reservations_path(1), {'reservations': reservation_details})


@worker_required('restaurant')
def delete_restaurant_reservation(request, pk):
    reservation = RestaurantReservation.objects.get(id=pk)
    reservation.is_active = False
    reservation.save()
    messages.success(request, "S'ha eliminat la reserva de restaurant amb èxit!")
    return redirect('restaurant_reservations')


@worker_required('restaurant')
def confirm_restaurant_reservation(request, pk):
    reservation = RestaurantReservation.objects.get(id=pk)
    reservation.client_arrived = 'client_arrived' in request.POST
    reservation.save()
    messages.success(request, "S'ha actualitzat la reserva de restaurant amb èxit!")
    return redirect('restaurant_reservations')
