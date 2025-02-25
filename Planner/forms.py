from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

from Reception.config import Config as c
from Reception.models import Room
from User.config import Config as uc


class RoomForm(forms.ModelForm):
    is_clean = forms.BooleanField(required=False)
    is_taken = forms.BooleanField(required=False)
    room_num = forms.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(699)])
    room_type = forms.ChoiceField(choices=c.get_room_types)

    class Meta:
        model = Room
        fields = ['room_num', 'room_type', 'is_clean', 'is_taken']

    def clean(self):
        cleaned_data = super().clean()
        room_num = cleaned_data.get('room_num')
        room_type = cleaned_data.get('room_type')

        room_types = [room[0] for room in c.get_room_types()]

        if room_type not in room_types or room_type == 'No seleccionat':
            raise ValidationError('El tipus d\'habitació seleccionat no és vàlid')

        try:
            valid_range = c.get_room_number_range(room_type)
            if not valid_range or not (valid_range[0] <= room_num <= valid_range[1]):
                raise ValidationError(f'El número d\'habitació per {room_type} ha de '
                                      f'ser entre {valid_range[0]} i {valid_range[1]}')
        except TypeError:
            raise ValidationError('El tipus d\'habitació seleccionat no és vàlid o no està ben configurat')

        if Room.objects.filter(room_num=room_num).exists():
            raise ValidationError('Aquest número d\'habitació ja està en ús')

        return cleaned_data


class CreateWorker(forms.Form):
    worker_type_choices = [(key, key.capitalize()) for key in uc.get_worker_type_to_url().keys()]

    worker_type = forms.ChoiceField(choices=worker_type_choices, label='Tipus de treballador')

    class Meta:
        fields = ['worker_type']

    def clean(self):
        cleaned_data = super().clean()
        worker_type = cleaned_data.get('worker_type')

        if worker_type not in uc.get_worker_type_to_url().keys():
            raise ValidationError('El tipus de treballador seleccionat no és vàlid')

        return cleaned_data
