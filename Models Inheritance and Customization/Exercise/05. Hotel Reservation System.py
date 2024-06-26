from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True

    def mark_as_unread(self):
        self.is_read = False

    def reply_to_message(self, reply_content, receiver1):
        return Message(sender=self.receiver, receiver=receiver1, content=reply_content)

    def forward_message(self, sender, receiver):
        return Message(sender=sender, receiver=receiver, content=self.content)


class StudentIDField(models.PositiveIntegerField):  # can get x < 0, so if error fix

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        value = int(value)
        return value

    def get_prep_value(self, value):
        return self.to_python(value)


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


class MaskedCreditCardField(models.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 20
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        for thing in value:
            try:
                int(thing)
            except ValueError:
                raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        final_string = f"****-****-****-{value[-4:]}"
        return final_string

    def get_prep_value(self, value):
        return self.to_python(value)


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()











class Hotel(models.Model):
    name = models.CharField(
        max_length=100,
    )

    address = models.CharField(
        max_length=200,
    )


class Room(models.Model):
    hotel = models.ForeignKey(
        to=Hotel,
        on_delete=models.CASCADE,
    )

    number = models.CharField(
        max_length=100,
        unique=True,
    )

    capacity = models.PositiveIntegerField()

    total_guests = models.PositiveIntegerField()

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    def clean(self) -> None:
        if self.total_guests > self.capacity:
            raise ValidationError("Total guests are more than the capacity of the room")

    def save(self, *args, **kwargs) -> str:
        self.clean()

        super().save(*args, **kwargs)

        return f"Room {self.number} created successfully"


class BaseReservation(models.Model):

    class Meta:
        abstract = True

    room = models.ForeignKey(
        to=Room,
        on_delete=models.CASCADE,
    )

    start_date = models.DateField()

    end_date = models.DateField()

    def reservation_period(self) -> int:
        return (self.end_date - self.start_date).days

    def calculate_total_cost(self) -> int:
        total_cost = self.reservation_period() * self.room.price_per_night

        return round(total_cost, 1)

    @property
    def is_available(self):
        reservations = self.__class__.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date,
        )

        return not reservations.exists()

    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError("Start date cannot be after or in the same end date")

        if not self.is_available:
            raise ValidationError(f"Room {self.room.number} cannot be reserved")


class RegularReservation(BaseReservation):
    def save(self, *args, **kwargs):
        super().clean()

        super().save(*args, **kwargs)

        return f"Regular reservation for room {self.room.number}"


class SpecialReservation(BaseReservation):
    def save(self, *args, **kwargs):
        super().clean()

        super().save(*args, **kwargs)

        return f"Special reservation for room {self.room.number}"

    def extend_reservation(self, days: int) -> str:
        # change the property is_available to method and add param days
        reservations = SpecialReservation.objects.filter(
            room=self.room,
            end_date__gte=self.start_date,
            start_date__lte=self.end_date + timedelta(days=days),
        )

        if reservations:
            raise ValidationError("Error during extending reservation")

        self.end_date += timedelta(days=days)
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
