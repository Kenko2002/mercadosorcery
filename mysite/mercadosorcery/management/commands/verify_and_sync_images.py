import os
from django.conf import settings
from django.core.management.base import BaseCommand
from mercadosorcery.models import Carta
from django.db.models import Q

class Command(BaseCommand):
    help = 'Finds any card with an image and applies it to all other printings of the same card that are missing an image.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO('Starting robust image synchronization process...'))
        
        cards_missing_image = Carta.objects.filter(Q(imagem__isnull=True) | Q(imagem=''))
        total_missing = cards_missing_image.count()
        self.stdout.write(f'Found {total_missing} cards missing an image. Attempting to sync...')
        
        synced_count = 0
        for target_card in cards_missing_image:
            try:
                # Encontra a primeira carta correspondente com o mesmo nome que TENHA uma imagem
                source_card = Carta.objects.exclude(Q(imagem__isnull=True) | Q(imagem='')).filter(
                    nome=target_card.nome
                ).first() # Pega a primeira que encontrar
                
                if source_card:
                    # Copia o caminho da imagem e salva
                    target_card.imagem = source_card.imagem
                    target_card.save()
                    synced_count += 1
                    self.stdout.write(self.style.SUCCESS(f'  - Synced "{target_card.nome}" ({target_card.printing}) from "{source_card.printing}" printing.'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  - An error occurred while syncing "{target_card.nome}": {e}'))

        self.stdout.write(self.style.SUCCESS(f'\nSync complete. {synced_count} of {total_missing} missing images were found and synced.'))
