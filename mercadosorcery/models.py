from django.db import models
from django.conf import settings

class Carta(models.Model):
    class Printing(models.TextChoices):
        ALPHA = "Alpha", "Alpha"
        ALPHA_FOIL = "Alpha (foil)", "Alpha (foil)"
        BETA = "Beta", "Beta"
        BETA_FOIL = "Beta (foil)", "Beta (foil)"
        ARTHURIAN_LEGENDS = "Arthurian_Legends", "Arthurian Legends"
        ARTHURIAN_LEGENDS_FOIL = "Arthurian_Legends (foil)", "Arthurian Legends (foil)"
        DRAGONLORDS = "Dragonlords", "Dragonlords"
        DRAGONLORDS_FOIL = "Dragonlords (foil)", "Dragonlords (foil)"
        GOTHIC = "Gothic", "Gothic"
        GOTHIC_FOIL = "Gothic (foil)", "Gothic (foil)"
        PROMOTIONAL = "Promotional", "Promotional"
        PROMOTIONAL_FOIL = "Promotional (foil)", "Promotional (foil)"

    nome = models.CharField(max_length=255)
    raridade = models.CharField(max_length=50)
    tipo = models.CharField(max_length=50)
    efeito = models.TextField()
    poder = models.IntegerField(blank=True, null=True)
    defesa = models.IntegerField(blank=True, null=True)
    custo_mana = models.IntegerField(default=0)
    treshold_agua = models.IntegerField(default=0)
    treshold_vento = models.IntegerField(default=0)
    treshold_fogo = models.IntegerField(default=0)
    treshold_terra = models.IntegerField(default=0)
    printing = models.CharField(max_length=100, choices=Printing.choices)

    def __str__(self):
        return f"{self.nome} ({self.printing})"

class Colecao(models.Model):
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cartas = models.ManyToManyField(Carta, through='Posse')

    def __str__(self):
        return f"Coleção de {self.usuario.first_name} {self.usuario.last_name}"

class Posse(models.Model):
    class Status(models.TextChoices):
        VENDENDO_PELO_PRECO_MEDIO = 'VENDENDO_PELO_PRECO_MEDIO', 'Vendendo_Pelo_Preco_Medio'
        VENDENDO_PELO_MENOR_PRECO = 'VENDENDO_PELO_MENOR_PRECO', 'Vendendo_Pelo_Menor_Preco'
        VENDENDO_PELO_PRECO_DEFINIDO = 'VENDENDO_PELO_PRECO_DEFINIDO', 'Vendendo_Pelo_Preco_Definido'
        FORA_DE_VENDA = 'FORA_DE_VENDA', 'Fora_De_Venda'

    class EstadoCarta(models.TextChoices):
        NEAR_MINT = 'NM', 'NearMint'
        SLIGHTLY_PLAYED = 'SP', 'Slightly Played'
        MODERATELY_PLAYED = 'MP', 'Moderatedly Played'
        HIGHLY_PLAYED = 'HP', 'Highly Played'
        DAMAGED = 'D', 'Damaged'

    carta = models.ForeignKey(Carta, on_delete=models.CASCADE)
    colecao = models.ForeignKey(Colecao, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.FORA_DE_VENDA)
    estado_carta = models.CharField(max_length=50, choices=EstadoCarta.choices, default=EstadoCarta.NEAR_MINT)
    preco_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.carta.nome} na coleção de {self.colecao.usuario.first_name} {self.colecao.usuario.last_name}"

class Lista(models.Model):
    nome = models.CharField(max_length=255)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cartas = models.ManyToManyField(Posse)

    def __str__(self):
        return self.nome
