# Generated by Django 2.2.7 on 2020-09-02 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0063_grupo_obligar_calificacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='opcioncalificacion',
            name='oculta',
            field=models.BooleanField(default=False, verbose_name='Ocultar'),
        ),
    ]