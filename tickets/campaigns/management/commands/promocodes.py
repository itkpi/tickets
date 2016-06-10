from uuid import uuid4

from django.core.management import BaseCommand

from campaigns.models import PromoCode, TicketType


class Command(BaseCommand):
    help = 'Generates promocodes'

    def add_arguments(self, parser):
        parser.add_argument('--tickettype', nargs='?', type=int, required=True)
        parser.add_argument('--count', nargs='?', type=int, required=True)

    def handle(self, *args, **options):
        ticket_type = TicketType.objects.get(id=options['tickettype'])
        promos = []
        for i in range(options['count']):
            promo = PromoCode.objects.create(uid=self.gen_uid(), ticket_type=ticket_type)
            promos.append(promo)
        for promo in promos:
            print(promo.get_absolute_url())

    def gen_uid(self):
        return "P-{}".format(uuid4())
