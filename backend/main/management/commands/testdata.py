from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from django.core.management.base import BaseCommand
from sports.models import Sport, Sporttype
from faker import Faker

User = get_user_model()


sporttypes = [
    Sporttype(id=1, title="Snowboarding"),
    Sporttype(id=2, title="Skiing"),
    Sporttype(id=3, title="Biking"),
    Sporttype(id=4, title="Surfing"),
    Sporttype(id=5, title="Diving"),
    Sporttype(id=6, title="Yoga"),
    Sporttype(id=7, title="Hiking"),
    Sporttype(id=8, title="Swimming"),
    Sporttype(id=9, title="Running"),
    Sporttype(id=10, title="Walking"),
    Sporttype(id=11, title="Snorkeling")
]

sportlevel = [
    '1',
    '2'
    '3'
]

is_guide = [
    True,
    False
]


class Command(BaseCommand):
    """
    Create Play Data in Dev
    """

    def handle(self, *args, **kwargs):

        if len(Sporttype.objects.all()) < 11:
            Sporttype.objects.bulk_create(sporttypes)

        x = 0
        user_to_create = 50
        while x < user_to_create:
            fake = Faker()
            # Create new User
            new_user = mixer.blend(User)

            # Randomize Guide or User
            is_guide_randomizer = fake.random_int(min=1, max=len(is_guide), step=1)
            new_user.profile.is_guide = is_guide[is_guide_randomizer - 1]
            new_user.save()

            y = 0

            while y < 5:
                # Create new Sport Number
                new_sport_id = fake.random_int(min=1, max=len(sporttypes), step=1)
                new_level = fake.random_int(min=1, max=3, step=1)

                if Sport.objects.filter(id=new_sport_id).exists() is False:
                    new_sport = sporttypes[new_sport_id - 1]
                    Sport.objects.create(
                        profile=new_user.profile,
                        sporttype=new_sport,
                        level=new_level
                    )
                y += 1

            x += 1
            self.stdout.write(self.style.SUCCESS(f'User ${x} of ${user_to_create} created'))

        self.stdout.write(self.style.SUCCESS('#############################'))
        self.stdout.write(self.style.SUCCESS('##   Test data created   ####'))
        self.stdout.write(self.style.SUCCESS('#############################'))
