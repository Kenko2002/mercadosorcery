from django.core.management.base import BaseCommand
from mercadosorcery.models import Carta

class Command(BaseCommand):
    help = 'Prints a list of all cards missing an image to standard output.'

    def handle(self, *args, **options):
        # Busca todas as cartas que não têm um caminho de imagem
        missing_images_cards = Carta.objects.filter(imagem__in=[None, '']).order_by('printing', 'nome')
        
        if not missing_images_cards.exists():
            self.stdout.write('All cards have images!')
        else:
            # Apenas imprime a saída. Não tenta escrever em arquivo.
            for carta in missing_images_cards:
                self.stdout.write(f"{carta.printing} - {carta.nome} (ID: {carta.id})")
