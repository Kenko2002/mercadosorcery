
import requests
from django.core.management.base import BaseCommand
from django.db import transaction
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Popula o banco de dados com cartas da API Curiosa'

    def handle(self, *args, **kwargs):
        # API URL correta
        url = 'https://api.curiosa.io/v1/cards'
        self.stdout.write("Buscando dados da API Curiosa...")
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            # A API retorna os dados sob a chave 'data'
            response_data = response.json()
            cards_data = response_data.get('data', [])
            
            self.stdout.write(f"Encontradas {len(cards_data)} cartas na API. Processando...")

            card_creations = 0
            card_updates = 0
            
            # Obter um conjunto de opções de printing válidas para uma busca rápida
            valid_printings = {choice[0] for choice in Carta.Printing.choices}

            # Usar uma transação para acelerar as operações de banco de dados
            with transaction.atomic():
                for card_data in cards_data:
                    card_name = card_data.get('name')
                    if not card_name:
                        continue

                    # Os atributos da carta estão no nível superior
                    elements = card_data.get('elements', [])
                    
                    # Iterar sobre cada printing da carta
                    for printing_info in card_data.get('printings', []):
                        edition = printing_info.get('edition')
                        if not edition:
                            continue
                        
                        # Normalizar o nome da edição para corresponder às choices do modelo
                        # ex: "Arthurian Legends" -> "Arthurian_Legends"
                        db_edition_name = edition.replace(' ', '_')

                        # Determinar o valor do printing (ex: "Beta" ou "Beta (foil)")
                        is_foil = printing_info.get('foil', False)
                        printing_value = f"{db_edition_name} (foil)" if is_foil else db_edition_name

                        # Verificar se o valor de printing gerado é válido
                        if printing_value not in valid_printings:
                            self.stdout.write(self.style.WARNING(f"Printing '{printing_value}' para '{card_name}' (edição '{edition}') não é uma opção válida. Pulando variante."))
                            continue
                            
                        # Preparar os dados para o modelo
                        defaults = {
                            'raridade': card_data.get('rarity') or '',
                            'tipo': card_data.get('type') or '',
                            'efeito': card_data.get('rulesText', ''),
                            'poder': card_data.get('attack'),
                            # A API usa 'health' para defesa
                            'defesa': card_data.get('health'),
                            'custo_mana': card_data.get('cost', 0) or 0,
                            # Determinar thresholds com base na lista 'elements'
                            'treshold_agua': 1 if 'Water' in elements else 0,
                            'treshold_vento': 1 if 'Air' in elements else 0,
                            'treshold_fogo': 1 if 'Fire' in elements else 0,
                            'treshold_terra': 1 if 'Earth' in elements else 0,
                        }

                        # Criar ou atualizar a entrada da carta
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
