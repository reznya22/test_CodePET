import random

from django.core.management import BaseCommand
from django.utils.crypto import get_random_string

from service.models import User, Reason, Collect, Payment


class Command(BaseCommand):
    help = "Generate random mock objects"

    def add_arguments(self, parser):
        parser.add_argument(
            'count',
            type=int,
            help='Indicates the number of objects to be created'
        )

    def handle(self, *args, **kwargs):
        count = kwargs.get('count')

        for _ in range(count):
            User.objects.create(username=get_random_string(length=15),
                                email=f'{get_random_string(length=10)}@tst.ru',
                                password='177899Test',
                                first_name=get_random_string(length=10),
                                last_name=get_random_string(length=10)
                                )
            Reason.objects.create(name=get_random_string(length=8))
            Collect.objects.create(author=random.choice(User.objects.all()),
                                   title=get_random_string(length=10),
                                   reason=random.choice(Reason.objects.all()),
                                   description=get_random_string(length=50),
                                   goal=random.randint(100, 10000000000),
                                   current_amount=random.randint(100,
                                                                 10000000),
                                   users_count=random.randint(0, 500)
                                   )
            Payment.objects.create(amount=random.randint(100, 100000000),
                                   user=random.choice(User.objects.all()),
                                   collect=random.choice(Collect.objects.all())
                                   )

        self.stdout.write(self.style.SUCCESS('Mock data has been created!'))
