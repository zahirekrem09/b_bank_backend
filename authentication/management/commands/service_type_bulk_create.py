from django.core.management import BaseCommand

from authentication.models import ServiceType


class Command(BaseCommand):
    help = "created for bulk operation"

    def handle(self, *args, **options):
        service_list = ["kapper", "schoonheidsspecialiste", "pedicure", "visagist",
                        "styliste", "nagelstyliste", "haarwerken"]
        for service_name in service_list:
            ServiceType.objects.get_or_create(name=service_name)


# map(lambda x: MyModel.objects.get_or_create(name=x), items)
