# Generated by Django 2.2.7 on 2020-10-02 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0062_rename_backlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='obligar_calificacion',
            field=models.BooleanField(default=False, verbose_name='Forzar calificación'),
        ),
    ]