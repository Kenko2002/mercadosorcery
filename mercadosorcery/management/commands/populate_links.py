
import requests
from django.core.management.base import BaseCommand
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Populates the database with card image links from an external API'

    def handle(self, *args, **options):
        if Carta.objects.exists():
            self.stdout.write(self.style.SUCCESS('Cards already exist in the database. Skipping population.'))
            return

        self.stdout.write(self.style.SUCCESS('Fetching card data from API...'))
        # Replace with the actual API endpoint
        api_url = 'https://api.sorcerytcg.com/cards'
        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from API: {e}'))
            return

        self.stdout.write(self.style.SUCCESS('Populating database with card image links...'))
        for card_data in data:
            # Map API data to your model fields
            Carta.objects.create(
                nome=card_data.get('name'),
                raridade=card_data.get('rarity'),
                tipo=card_data.get('type'),
                efeito=card_data.get('effect_text'),
                poder=card_data.get('power'),
                defesa=card_data.get('life'),
                custo_mana=card_data.get('mana_cost'),
                treshold_agua=card_data.get('elemental_power', {}).get('water'),
                treshold_vento=card_data.get('elemental_power', {}).get('air'),
                treshold_fogo=card_data.get('elemental_power', {}).get('fire'),
                treshold_terra=card_data.get('elemental_power', {}).get('earth'),
                printing=card_data.get('card_finish'),
                link_imagem=card_data.get('image_url')
            )
        self.stdout.write(self.style.SUCCESS('Successfully populated card image links.'))

