# Generated by Django 3.0.5 on 2020-07-27 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20200727_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='observacao',
            field=models.CharField(blank=True, max_length=1000, verbose_name='Observação'),
        ),
    ]
