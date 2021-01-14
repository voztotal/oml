# Generated by Django 2.2.7 on 2020-12-18 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0069_regla_incidencia_por_calificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parametroscrm',
            name='tipo',
            field=models.PositiveIntegerField(choices=[
                (1, 'Dato de Campaña'),
                (2, 'Dato de Contacto'),
                (3, 'Dato de Llamada'),
                (4, 'Fijo'),
                (5, 'Dato de Dialplan')]),
        ),
    ]