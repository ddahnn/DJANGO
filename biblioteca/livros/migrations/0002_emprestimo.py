# Generated by Django 5.2.1 on 2025-05-28 05:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livros', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emprestimo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_retirada', models.DateField(auto_now_add=True)),
                ('data_prevista_entrega', models.DateField()),
                ('data_devolucao', models.DateField(blank=True, null=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livros.cliente')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='livros.livros')),
            ],
        ),
    ]
