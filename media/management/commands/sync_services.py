from django.core.management.base import BaseCommand

from media.models import Service
from media.tmdb import get_services_list_from_api

WATCH_PROVIDERS_MOVIE = "/watch/providers/movie"


class Command(BaseCommand):
    help = "Sync the streaming services catalog from TMDB into the DB"

    def handle(self, *args, **options):
        services = get_services_list_from_api(WATCH_PROVIDERS_MOVIE)

        if services:
            for service in services:
                Service.objects.update_or_create(
                    tmdb_provider_id=service["provider_id"],
                    defaults={
                        "name": service["provider_name"],
                        "logo_path": service.get("logo_path", ""),
                        "display_priority": service.get("display_priority", 0),
                    },
                )
            self.stdout.write(f"Synced {len(services)} services from TMDB.")
        else:
            self.stdout.write("No services returned from TMDB.")
