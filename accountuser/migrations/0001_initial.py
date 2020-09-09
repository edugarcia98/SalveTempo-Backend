# Generated by Django 3.0.5 on 2020-09-09 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='E-mail')),
                ('username', models.CharField(max_length=30, verbose_name='Usuário')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Data de Entrada')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Último Login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
