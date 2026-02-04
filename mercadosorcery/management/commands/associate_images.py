
import os
import re
from django.core.management.base import BaseCommand
from django.conf import settings
from mercadosorcery.models import Carta

def normalize_name(name):
    """Converts to lowercase and removes all non-alphanumeric characters."""
    if not name:
        return ""
    return re.sub(r'[^a-z0-9]', '', name.lower())

class Command(BaseCommand):
    help = 'Associa imagens de arquivos a cartas no banco de dados sem usar dependências externas de fuzzy matching.'

    def handle(self, *args, **options):
        image_folder_path = os.path.join(settings.BASE_DIR, 'imagens_comprimidas')
        
        if not os.path.isdir(image_folder_path):
            self.stdout.write(self.style.ERROR(f'Diretório de imagens não encontrado: {image_folder_path}'))
            return

        self.stdout.write('Limpando associações de imagens existentes...')
        Carta.objects.all().update(imagem=None)
        self.stdout.write(self.style.SUCCESS('Associações de imagens anteriores foram limpas.'))

        all_image_files = os.listdir(image_folder_path)
        self.stdout.write(f'{len(all_image_files)} imagens encontradas para processar.')

        printing_map = {
            'bet': ('Alpha', 'Alpha (foil)', 'Beta', 'Beta (foil)'),
            'art': ('Arthurian_Legends', 'Arthurian_Legends (foil)'),
            'dra': ('Dragonlords', 'Dragonlords (foil)'),
            'got': ('Gothic', 'Gothic (foil)'),
            'pro': ('Promotional', 'Promotional (foil)'),
        }

        # Cache all relevant cards from the database, normalized
        # This avoids querying the DB inside the loop
        cards_by_printing = {}
        all_printings = [p for sublist in printing_map.values() for p in sublist]
        all_cards = Carta.objects.filter(printing__in=all_printings)
        
        normalized_card_map = {}
        for card in all_cards:
            normalized_name = normalize_name(card.nome)
            if normalized_name not in normalized_card_map:
                normalized_card_map[normalized_name] = []
            normalized_card_map[normalized_name].append(card)

        self.stdout.write(f"Mapeamento de {len(normalized_card_map)} nomes de cartas normalizados criado.")

        # Process each image file
        for image_name in all_image_files:
            match = re.match(r"^([a-z]{3})-([a-zA-Z0-9_]+)((?:-[a-z0-9_]+)*)\.png$", image_name)
            if not match:
                self.stdout.write(self.style.WARNING(f'Ignorando arquivo com formato inesperado: {image_name}'))
                continue

            printing_code, card_name_part, _ = match.groups()
            possible_printings = printing_map.get(printing_code)

            if not possible_printings:
                self.stdout.write(self.style.WARNING(f'Prefixo de edição não mapeado ignorado: {printing_code} no arquivo {image_name}'))
                continue

            normalized_name_from_file = normalize_name(card_name_part)
            
            # Find a match in our pre-built map
            matched_cards = normalized_card_map.get(normalized_name_from_file)

            if matched_cards:
                # We found a match. Get the canonical name from the first matched card.
                canonical_name = matched_cards[0].nome
                
                # Find all versions of this card that should be updated
                # (i.e., those that share the same canonical name and are in the correct printings)
                absolute_image_path = os.path.join(image_folder_path, image_name)
                updated_count = Carta.objects.filter(
                    nome=canonical_name,
                    printing__in=possible_printings
                ).update(imagem=absolute_image_path)

                if updated_count > 0:
                    self.stdout.write(self.style.SUCCESS(
                        f'[OK] Imagem "{image_name}" associada a {updated_count} versão(ões) de "{canonical_name}".'
                    ))
                else:
                    # This case should be rare, but good to log
                    self.stdout.write(self.style.NOTICE(
                        f'[AVISO] Uma correspondência foi encontrada para "{image_name}", mas nenhuma carta foi atualizada.'
                    ))
            else:
                self.stdout.write(self.style.WARNING(
                    f'[FALHA] Nenhuma correspondência no banco de dados para a imagem "{image_name}" (Nome normalizado: {normalized_name_from_file})'
                ))

        self.stdout.write(self.style.SUCCESS('Processo de associação de imagens concluído.'))
