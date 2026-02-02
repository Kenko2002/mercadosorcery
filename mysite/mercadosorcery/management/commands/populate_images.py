
import requests
import time
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Popula o banco de dados com imagens das cartas da API do Sorcery TCG'

    def handle(self, *args, **kwargs):
        IMAGE_BASE_URL = 'https://sorcery-production.s3.amazonaws.com/cards/{slug}.png'
        API_URL = 'https://api.sorcerytcg.com/api/cards'
        self.stdout.write("Buscando dados da API do Sorcery TCG para imagens...")
        
        try:
            response = requests.get(API_URL)
            response.raise_for_status()
            cards_data = response.json()
            self.stdout.write(f"Encontradas {len(cards_data)} cartas na API. Processando imagens...")

            image_downloads = 0
            image_skipped = 0
            cards_not_found = 0

            valid_printings = [choice[0] for choice in Carta.Printing.choices]

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

                    db_set_name = set_name_api.replace(' ', '_')

                    for variant_data in set_data.get('variants', []):
                        slug = variant_data.get('slug')
                        if not slug:
                            continue

                        finish = variant_data.get('finish')
                        
                        printing_value = db_set_name
                        if finish == 'Foil':
                            printing_value = f"{db_set_name} (foil)"
                        
                        if printing_value not in valid_printings:
                            continue

                        try:
                            carta = Carta.objects.get(nome=card_name, printing=printing_value)

                            if carta.imagem:
                                image_skipped += 1
                                continue

                            image_url = IMAGE_BASE_URL.format(slug=slug)
                            self.stdout.write(f"Baixando imagem para: {carta}")
                            
                            img_response = requests.get(image_url)
                            img_response.raise_for_status()
                            
                            file_name = f'{slug}.png'
                            carta.imagem.save(file_name, ContentFile(img_response.content), save=True)
                            
                            image_downloads += 1
                            time.sleep(0.1)

                        except Carta.DoesNotExist:
                            self.stdout.write(self.style.WARNING(f"Carta não encontrada no BD: {card_name} ({printing_value})."))
                            cards_not_found += 1
                        except requests.exceptions.HTTPError as e:
                            if e.response.status_code == 404:
                                self.stdout.write(self.style.WARNING(f"Imagem não encontrada em {image_url} (404). Pulando."))
                            else:
                                self.stdout.write(self.style.ERROR(f"Erro HTTP ao baixar {image_url}: {e}"))
            
            self.stdout.write(self.style.SUCCESS(f'Processamento de imagens concluído. {image_downloads} imagens baixadas, {image_skipped} imagens puladas (já existiam).'))
            if cards_not_found > 0:
                self.stdout.write(self.style.WARNING(f'{cards_not_found} cartas referenciadas na API não foram encontradas no banco de dados.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Erro ao buscar dados da API: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocorreu um erro inesperado: {e}'))
