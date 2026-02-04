from django.core.management.base import BaseCommand
from django.db.models import Q
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Syncs missing card images between ALP and BET printings.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting image sync process between ALP and BET...'))
        
        synced_count = 0

        # 1. Sync from BET to ALP
        alp_missing_image = Carta.objects.filter(printing='ALP', imagem__in=[None, ''])
        self.stdout.write(f'Found {alp_missing_image.count()} cards in ALP missing images.')

        for carta_alp in alp_missing_image:
            try:
                # Find corresponding BET card with an image
                carta_bet = Carta.objects.exclude(imagem__in=[None, '']).get(nome=carta_alp.nome, printing='BET')
                self.stdout.write(f'Found image for "{carta_alp.nome}" in BET. Syncing to ALP.')
                carta_alp.imagem = carta_bet.imagem
                carta_alp.save()
                synced_count += 1
            except Carta.DoesNotExist:
                continue
            except Carta.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'Found multiple BET cards for "{carta_alp.nome}". Skipping.'))
                continue

        # 2. Sync from ALP to BET
        bet_missing_image = Carta.objects.filter(printing='BET', imagem__in=[None, ''])
        self.stdout.write(f'Found {bet_missing_image.count()} cards in BET missing images.')
        
        for carta_bet in bet_missing_image:
            try:
                # Find corresponding ALP card with an image
                carta_alp = Carta.objects.exclude(imagem__in=[None, '']).get(nome=carta_bet.nome, printing='ALP')
                self.stdout.write(f'Found image for "{carta_bet.nome}" in ALP. Syncing to BET.')
                carta_bet.imagem = carta_alp.imagem
                carta_bet.save()
                synced_count += 1
            except Carta.DoesNotExist:
                continue
            except Carta.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f'Found multiple ALP cards for "{carta_bet.nome}". Skipping.'))
                continue

        self.stdout.write(self.style.SUCCESS(f'Image sync process complete. {synced_count} images were synced.'))
