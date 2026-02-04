
import requests
from django.core.management.base import BaseCommand
from mercadosorcery.models import Carta
from django.db import transaction

class Command(BaseCommand):
    help = 'Populates or updates the database with card data and image links from an external API'

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Fetching card data from API...'))
        api_url = 'https://api.sorcerytcg.com/cards'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            all_card_data = response.json()
        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Failed to fetch data from API: {e}'))
            return

        self.stdout.write(self.style.SUCCESS(f'Processing {len(all_card_data)} cards from API...'))
        
        updated_count = 0
        created_count = 0

        for card_data in all_card_data:
            printing_value = card_data.get('card_finish')
            card_name = card_data.get('name')

            card_defaults = {
                'raridade': card_data.get('rarity'),
                'tipo': card_data.get('type'),
                'efeito': card_data.get('effect_text'),
                'poder': card_data.get('power'),
                'defesa': card_data.get('life'),
                'custo_mana': card_data.get('mana_cost'),
                'treshold_agua': card_data.get('elemental_power', {}).get('water'),
                'treshold_vento': card_data.get('elemental_power', {}).get('air'),
                'treshold_fogo': card_data.get('elemental_power', {}).get('fire'),
                'treshold_terra': card_data.get('elemental_power', {}).get('earth'),
                'link_imagem': card_data.get('image_url')
            }

            obj, created = Carta.objects.update_or_create(
                nome=card_name,
                printing=printing_value,
                defaults=card_defaults
            )

            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'Database population complete. {created_count} cards created, {updated_count} cards updated.'
        ))
