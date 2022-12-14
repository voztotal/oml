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

from django.db import models
from .mixins import AuditableModelMixin
from django.utils.translation import ugettext_lazy as _
from configuracion_telefonia_app.models import DestinoEntrante


class ConfiguracionProveedor(AuditableModelMixin, models.Model):
    TIPO_TWILIO = 0
    TIPO_META = 1
    TIPO_GUPSHUP = 2
    PROVEEDOR_TIPOS = (
        (TIPO_TWILIO, _('Twilio')),
        (TIPO_META, _('Meta')),
        (TIPO_GUPSHUP, _('GupShup'))
    )
    nombre = models.CharField(max_length=100)
    tipo_proveedor = models.IntegerField(choices=PROVEEDOR_TIPOS)
    identificador = models.CharField(max_length=100)
    token_autorizacion = models.CharField(max_length=250)


class Linea(AuditableModelMixin, models.Model):
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey(
        ConfiguracionProveedor, on_delete=models.CASCADE, related_name="lineas")
    numero = models.CharField(max_length=100)
    identificador = models.CharField(max_length=100)
    es_verificado = models.BooleanField(default=False)
    token_validacion = models.CharField(max_length=100)
    destino = models.ForeignKey(
        DestinoEntrante, on_delete=models.CASCADE, related_name="lineas", blank=True, null=True)
    mensaje_bienvenida = models.TextField(blank=True, null=True)
    mensaje_despedida = models.TextField(blank=True, null=True)
