# Generated by Django 2.2.7 on 2021-02-23 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0073_configuraciondeagentesdecampana'),
    ]

    operations = [
        migrations.AddField(
            model_name='grupo',
            name='call_off_camp',
            field=models.BooleanField(default=False, verbose_name='Llamada fuera de campaña'),
        ),
    ]
