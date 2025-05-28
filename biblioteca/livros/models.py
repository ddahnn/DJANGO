from django.db import models
from django.utils import timezone
from datetime import timedelta

# Create your models here.
class Autor(models.Model):
    nome = models.CharField(max_length=100)
    pais_Origem = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    

class Livros(models.Model):
    isbn = models.CharField(max_length=13, unique=True)
    nome = models.CharField(max_length=200)
    autores = models.ManyToManyField(Autor)  
    editora = models.CharField(max_length=100)
    ano_publicacao = models.IntegerField()
    disponivel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome
    

class Cliente(models.Model):
    matricula = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome
    


class Emprestimo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livros, on_delete=models.CASCADE)
    data_retirada = models.DateField(auto_now_add=True)  # hoje
    data_prevista_entrega = models.DateField()
    data_devolucao = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Se for um novo empréstimo
        if not self.pk:
            # Máximo de 3 livros por cliente
            emprestimos_ativos = Emprestimo.objects.filter(
                cliente=self.cliente,
                data_devolucao__isnull=True
            ).count()

            if emprestimos_ativos >= 3:
                raise ValueError("Cliente já possui 3 livros emprestados!")

            # O livro deve estar disponível
            if not self.livro.disponivel:
                raise ValueError("Livro não está disponível para empréstimo!")

            # Definindo data prevista de entrega (7 dias depois)
            self.data_prevista_entrega = timezone.now().date() + timedelta(days=7)

            # Atualiza a disponibilidade do livro
            self.livro.disponivel = False
            self.livro.save()

        # Se for devolução, o livro volta a ficar disponível
        if self.data_devolucao and not self.livro.disponivel:
            self.livro.disponivel = True
            self.livro.save()

        super().save(*args, **kwargs)

    def dias_atraso(self):
        if self.data_devolucao and self.data_devolucao > self.data_prevista_entrega:
            return (self.data_devolucao - self.data_prevista_entrega).days
        return 0

    def __str__(self):
        return f"{self.cliente.nome} -> {self.livro.nome}"