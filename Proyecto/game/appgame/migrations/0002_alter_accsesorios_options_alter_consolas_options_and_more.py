# Generated by Django 5.0.6 on 2024-07-16 04:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appgame', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='accsesorios',
            options={'ordering': ['nombre'], 'verbose_name': 'Accesorio', 'verbose_name_plural': 'Accesesorios'},
        ),
        migrations.AlterModelOptions(
            name='consolas',
            options={'ordering': ['-nombre'], 'verbose_name': 'Consala', 'verbose_name_plural': 'Consolas'},
        ),
        migrations.AlterModelOptions(
            name='juegos',
            options={'ordering': ['nombre'], 'verbose_name': 'Juego', 'verbose_name_plural': 'Juegos'},
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='avatares')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
