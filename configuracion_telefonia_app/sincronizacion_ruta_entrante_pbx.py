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

from __future__ import unicode_literals
import logging
from django.conf import settings
from django.db import connections, ProgrammingError
from configuracion_telefonia_app.models import RutaEntrante


class SincronizadorDeConfiguracionRutaEntrantePBX(object):
    """Sincroniza configuraciones de Rutas entrantes en una tabla del PBX"""

    def configuracion_ok(self):
        return ('pbx_database' in settings.DATABASES) and \
            'NAME' in settings.DATABASES['pbx_database'] and \
            len(settings.PBX_DATABASE_TABLE) > 0 and \
            len(settings.PBX_DATABASE_FIELD) > 0

    def agregar(self, ruta_entrante):
        if settings.SINCRONIZAR_INR_CON_PBX:
            if not self.configuracion_ok():
                return 'Error de configuración de base de datos del PBX.'
            return self._efectuar_adicion(ruta_entrante)
        return None

    def _efectuar_adicion(self, ruta_entrante):
        error = None
        sql = """
            INSERT INTO {tabla} ({campo}) VALUES ('{did}')
        """.format(**{
            'tabla': settings.PBX_DATABASE_TABLE,
            'campo': settings.PBX_DATABASE_FIELD,
            'did': ruta_entrante.telefono
        })
        cursor = connections['pbx_database'].cursor()
        try:
            cursor.execute(sql)
        except ProgrammingError, e:
            error = e.message
        return error

    def eliminar(self, ruta_entrante):
        if settings.SINCRONIZAR_INR_CON_PBX:
            if not self.configuracion_ok():
                return 'Error de configuración de base de datos del PBX.'
            return self._efectuar_eliminacion(ruta_entrante)
        return None

    def _efectuar_eliminacion(self, ruta_entrante):
        error = None
        sql = """
            DELETE FROM {tabla} WHERE {campo}='{did}'
        """.format(**{
            'tabla': settings.PBX_DATABASE_TABLE,
            'campo': settings.PBX_DATABASE_FIELD,
            'did': ruta_entrante.telefono
        })
        cursor = connections['pbx_database'].cursor()
        try:
            cursor.execute(sql)
        except ProgrammingError, e:
            logging.info(
                "Error al intentar eliminar rutas entrantes en la base de datos del PBX")
            error = e.message
        return error

    def sincronizar_todas(self):
        if settings.SINCRONIZAR_INR_CON_PBX:
            if self.configuracion_ok():
                error = None
                dids = RutaEntrante.objects.all().values_list('telefono', flat=True)
                if len(dids) > 0:
                    # Borro las que se que pueden estar para no insertar duplicados.
                    dids_txt = ', '.join(["'%s'" % x for x in dids])
                    sql = """
                        DELETE FROM {tabla} WHERE {campo} IN ({dids})
                    """.format(**{
                        'tabla': settings.PBX_DATABASE_TABLE,
                        'campo': settings.PBX_DATABASE_FIELD,
                        'dids': dids_txt
                    })
                    cursor = connections['pbx_database'].cursor()
                    try:
                        cursor.execute(sql)
                    except ProgrammingError, e:
                        error = e.message
                        return error

                    # Agrego las rutas entrantes
                    dids_txt = ', '.join(["('%s')" % x for x in dids])
                    sql = """
                        INSERT INTO {tabla} ({campo}) VALUES {dids}
                    """.format(**{
                        'tabla': settings.PBX_DATABASE_TABLE,
                        'campo': settings.PBX_DATABASE_FIELD,
                        'dids': dids_txt
                    })
                    cursor = connections['pbx_database'].cursor()
                    try:
                        cursor.execute(sql)
                    except ProgrammingError, e:
                        error = e.message
                    return error
            else:
                return 'No esta bien configurado para sincronizar INR en PBX.'
        else:
            return 'No esta bien configurado para sincronizar INR en PBX.'
