from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Obtém o modelo de usuário ativo, que é o nosso SocialEntity
User = settings.AUTH_USER_MODEL

# --- Modelo de Perfil (Sua arquitetura) ---

class Usuario(models.Model):
    class Role(models.TextChoices):
        PACIENTE = 'PACIENTE', 'Paciente'
        MEDICO = 'MEDICO', 'Medico'

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    cpf = models.CharField('CPF', max_length=11, unique=True, null=True, blank=True)
    imagem = models.ImageField(upload_to='imagens_perfil/', blank=True, null=True)
    role = models.CharField('função', max_length=50, choices=Role.choices, null=True, blank=True)

    def __str__(self):
        return self.user.email

# --- Sinal para criação automática de perfil ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Usuario.objects.create(user=instance)
    # O `hasattr` previne um erro caso o perfil ainda não tenha sido criado em certas chamadas
    if hasattr(instance, 'usuario'):
        instance.usuario.save()

# --- Modelos Originais (Restaurados) ---

class Carta(models.Model):
    nome = models.CharField(max_length=255)
    printing = models.CharField(max_length=10)
    imagem = models.CharField(max_length=512, blank=True, null=True)
    mana_cost = models.CharField(max_length=50, blank=True)
    cmc = models.FloatField(default=0.0)
    type_line = models.CharField(max_length=255, blank=True)
    oracle_text = models.TextField(blank=True)
    power = models.CharField(max_length=10, blank=True)
    toughness = models.CharField(max_length=10, blank=True)
    rarity = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.printing})"

class Colecao(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Coleção de {self.usuario.email}"

class Posse(models.Model):
    class EstadoCarta(models.TextChoices):
        NEAR_MINT = 'NM', 'Near Mint'
        LIGHTLY_PLAYED = 'LP', 'Lightly Played'
        MODERATELY_PLAYED = 'MP', 'Moderately Played'
        HEAVILY_PLAYED = 'HP', 'Heavily Played'
        DAMAGED = 'DM', 'Damaged'

    class Status(models.TextChoices):
        FORA_DE_VENDA = 'NOT_FOR_SALE', 'Fora de Venda'
        A_VENDA = 'FOR_SALE', 'À Venda'
        TROCANDO = 'TRADING', 'Trocando'

    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    colecao = models.ForeignKey(Colecao, on_delete=models.CASCADE)
    estado_carta = models.CharField(max_length=2, choices=EstadoCarta.choices)
    status = models.CharField(max_length=20, choices=Status.choices)
    preco_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Cópia de {self.carta.nome}"

class Lista(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cartas = models.ManyToManyField(Posse) # Baseado no seu serializer

    def __str__(self):
        return f"Lista '{self.nome}' de {self.usuario.email}"
