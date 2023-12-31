# -*- coding: utf-8 -*-
# Copyright (C) 2018 Freetech Solutions

# This file is part of OMniLeads

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3, as published by
# the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#
# Generated by Django 2.2.7 on 2020-03-12 11:00

from __future__ import unicode_literals

import json
from django.db import migrations


def corregir_campos_bd_contacto(apps, schema_editor):
    """
    Corrige los campos con espacios en las bases de datos de contactos
    """
    BaseDatosContacto = apps.get_model("ominicontacto_app", "BaseDatosContacto")
    for bd in BaseDatosContacto.objects.filter(metadata__isnull=False):
        metadata = json.loads(bd.metadata)
        metadata['nombres_de_columnas'] = [x.strip() for x in metadata['nombres_de_columnas']]
        bd.metadata = json.dumps(metadata)
        bd.save()


class Migration(migrations.Migration):

    dependencies = [
        ('ominicontacto_app', '0041_queue_musiconhold_playlist'),
    ]

    operations = [
        migrations.RunPython(corregir_campos_bd_contacto, reverse_code=migrations.RunPython.noop),
    ]
