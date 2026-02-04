
import gdown
import os
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Baixa todas as imagens de uma pasta do Google Drive.'

    def handle(self, *args, **kwargs):
        # URL da pasta compartilhada no Google Drive
        google_drive_url = 'https://drive.google.com/drive/folders/17IrJkRGmIU9fDSTU2JQEU9JlFzb5liLJ'
        
        # Diretório onde as imagens serão salvas
        output_folder = os.path.join(settings.BASE_DIR, 'imagens_gdrive')

        self.stdout.write(f"Iniciando o download da pasta do Google Drive...")
        self.stdout.write(f"URL: {google_drive_url}")
        self.stdout.write(f"Diretório de saída: {output_folder}")

        # Verifica se o diretório de saída existe, se não, cria
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
            self.stdout.write(self.style.SUCCESS(f"Diretório '{output_folder}' criado."))

        try:
            # Faz o download da pasta
            gdown.download_folder(google_drive_url, output=output_folder, quiet=False, use_cookies=False)
            self.stdout.write(self.style.SUCCESS("Download concluído com sucesso!"))
            self.stdout.write(f"As imagens foram salvas em: {output_folder}")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ocorreu um erro durante o download: {e}"))
            self.stdout.write(self.style.WARNING("Por favor, verifique se a URL do Google Drive está correta e se a pasta está com o compartilhamento 'Qualquer pessoa com o link pode ver'."))

