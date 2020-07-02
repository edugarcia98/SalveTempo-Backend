# Generated by Django 3.0.5 on 2020-07-01 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='especializacao',
            name='doencas',
        ),
        migrations.AddField(
            model_name='doenca',
            name='especializacoes',
            field=models.ManyToManyField(through='app.EspecializacaoDoenca', to='app.Especializacao', verbose_name='Especializações'),
        ),
    ]
