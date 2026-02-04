
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Popula o banco de dados com cartas da API do Sorcery TCG'

    def handle(self, *args, **kwargs):
        url = 'https://api.sorcerytcg.com/api/cards'
        self.stdout.write("Buscando dados da API do Sorcery TCG...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            cards_data = response.json()
            self.stdout.write(f"Encontradas {len(cards_data)} cartas na API. Processando...")

            card_creations = 0
            card_updates = 0
            
            valid_printings = {choice[0] for choice in Carta.Printing.choices}

            with transaction.atomic():
                for card_data in cards_data:
                    card_name = card_data.get('name')
                    if not card_name:
                        continue

                    for set_data in card_data.get('sets', []):
                        set_name_api = set_data.get('name')
                        if not set_name_api:
                            continue
                        
                        if set_name_api == 'Dragonlord':
                            set_name_api = 'Dragonlords'
                            
                        metadata = set_data.get('metadata', {})
                        db_set_name = set_name_api.replace(' ', '_')

                        for variant_data in set_data.get('variants', []):
                            finish = variant_data.get('finish')
                            
                            printing_value = db_set_name
                            if finish == 'Foil':
                                printing_value = f"{db_set_name} (foil)"
                            
                            if printing_value not in valid_printings:
                                self.stdout.write(self.style.WARNING(f"Printing '{printing_value}' para '{card_name}' (set '{set_name_api}') não é uma opção válida. Pulando variante."))
                                continue
                                
                            cost = metadata.get('cost')
                            
                            defaults = {
                                'raridade': metadata.get('rarity') or '',
                                'tipo': metadata.get('type') or '',
                                'efeito': metadata.get('rulesText', ''),
                                'poder': metadata.get('attack'),
                                'defesa': metadata.get('defence'),
                                'custo_mana': cost if cost is not None else 0,
                                'treshold_agua': metadata.get('thresholds', {}).get('water', 0),
                                'treshold_vento': metadata.get('thresholds', {}).get('air', 0),
                                'treshold_fogo': metadata.get('thresholds', {}).get('fire', 0),
                                'treshold_terra': metadata.get('thresholds', {}).get('earth', 0),
                            }

                            obj, created = Carta.objects.update_or_create(
                                nome=card_name,
                                printing=printing_value,
                                defaults=defaults
                            )

                            if created:
                                card_creations += 1
                            else:
                                card_updates += 1

            self.stdout.write(self.style.SUCCESS(f'Processamento concluído. {card_creations} cartas adicionadas, {card_updates} cartas atualizadas.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar dados da API: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado: {e}'))

