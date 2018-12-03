# -*- coding: utf-8 -*-
# Copyright (C) 2018 Freetech Solutions

# This file is part of OMniLeads

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
#

import logging

from django.core.management.base import BaseCommand

from configuracion_telefonia_app.sincronizacion_ruta_entrante_pbx import (
    SincronizadorDeConfiguracionRutaEntrantePBX)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Sincroniza las entradas de la tabla de rutas entrantes de PBX de acuerdo a la configuracion
    """

    help = u'Sincroniza las rutas entrantes con la tabla de rutas entrantes del PBX'

    def _sincronizar_rutas_entrantes(self):
        sincronizador = SincronizadorDeConfiguracionRutaEntrantePBX()
        return sincronizador.sincronizar_todas()

    def handle(self, *args, **options):
        try:
            error = self._sincronizar_rutas_entrantes()
        except Exception as e:
            logging.error('Fallo del comando: {0}'.format(e.message))
        if error:
            logging.error('Cuidado con el siguiente error: {0}'.format(error))
