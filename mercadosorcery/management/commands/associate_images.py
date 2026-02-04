
import os
import re
from django.core.management.base import BaseCommand
from thefuzz import fuzz
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Associa imagens às cartas (versões normais e foil) e usa busca por similaridade.'

    def handle(self, *args, **options):
        image_folder_path = '/home/user/exemploflutterflow/imagens_comprimidas'
        SIMILARITY_THRESHOLD = 70

        if not os.path.isdir(image_folder_path):
            self.stdout.write(self.style.ERROR(f'Diretório não encontrado: {image_folder_path}'))
            return

        self.stdout.write('Limpando associações de imagens existentes...')
        Carta.objects.all().update(imagem=None)
        self.stdout.write(self.style.SUCCESS('Associações limpas.'))

        all_image_files = os.listdir(image_folder_path)
        self.stdout.write(f'{len(all_image_files)} imagens encontradas para processar.')

        printing_map = {
            'alp': ('Alpha', 'Alpha (foil)'),
            'bet': ('Beta', 'Beta (foil)'),
            'art': ('Arthurian_Legends', 'Arthurian_Legends (foil)'),
            'dra': ('Dragonlords', 'Dragonlords (foil)'),
            'got': ('Gothic', 'Gothic (foil)'),
            'pro': ('Promotional', 'Promotional (foil)'),
        }

        for image_name in all_image_files:
            match = re.match(r"^([a-z]{3})-([a-zA-Z0-9_]+)((?:-[a-z0-9_]+)*)\.png$", image_name)
            if not match:
                self.stdout.write(self.style.WARNING(f'Formato de arquivo inesperado, ignorando: {image_name}'))
                continue

            printing_code, card_name_part, _ = match.groups()
            card_name_from_file = card_name_part.replace('_', ' ').title()
            possible_printings = printing_map.get(printing_code)

            if not possible_printings:
                self.stdout.write(self.style.WARNING(f'Prefixo de edição não mapeado: {printing_code}'))
                continue

            target_card_name = None

            # 1. Tenta correspondência exata.
            exact_match_q = Carta.objects.filter(nome__iexact=card_name_from_file, printing__in=possible_printings)
            if exact_match_q.exists():
                target_card_name = exact_match_q.first().nome
                self.stdout.write(self.style.SUCCESS(f'[Exato] Nome base encontrado: "{target_card_name}" para o arquivo {image_name}'))
            else:
                # 2. Se falhar, busca por similaridade (compatível com todos os bancos de dados).
                unique_card_names_qs = Carta.objects.filter(printing__in=possible_printings).values_list('nome', flat=True).distinct()
                
                highest_score = 0
                best_match_name = ""

                for db_card_name in unique_card_names_qs:
                    score = fuzz.ratio(card_name_from_file.lower(), db_card_name.lower())
                    if score > highest_score:
                        highest_score = score
                        best_match_name = db_card_name

                if highest_score >= SIMILARITY_THRESHOLD:
                    target_card_name = best_match_name
                    self.stdout.write(self.style.SUCCESS(
                        f'[Similaridade] Nome base encontrado: "{target_card_name}" para o arquivo {image_name} (Score: {highest_score}%)'
                    ))

            # 3. Se um nome de carta foi encontrado, atualiza todas as suas versões (normal e foil).
            if target_card_name:
                absolute_image_path = os.path.join(image_folder_path, image_name)
                updated_count = Carta.objects.filter(
                    nome__iexact=target_card_name,
                    printing__in=possible_printings
                ).update(imagem=absolute_image_path)

                if updated_count > 0:
                    self.stdout.write(f'--> Imagem associada a {updated_count} versão(ões) de "{target_card_name}".\n')
            else:
                self.stdout.write(self.style.WARNING(f'Nenhuma correspondência encontrada para o arquivo {image_name} (Busca: "{card_name_from_file}")\n'))

        self.stdout.write(self.style.SUCCESS('Processo de associação concluído.'))
