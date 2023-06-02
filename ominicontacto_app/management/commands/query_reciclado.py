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
from __future__ import unicode_literals

import logging.config

from django.core.management.base import BaseCommand
from django.db import connection
from reportes_app.models import LlamadaLog
from ominicontacto_app.models import Campana

# DEBUG -> T => python manage.py query_reciclado 2
# DEBUG -> F => OML_LOGGING_SLOWSQL_ENABLED=1 OML_LOGGING_SLOWSQL_OUTPUT=slowsql.txt python manage.py query_reciclado 2

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("camapana_id", nargs="+", type=int)
        parser.add_argument("query", nargs="+", type=int)

    def handle(self, *args, **options):
        campana = Campana.objects.get(id=options['camapana_id'][0])
        campana_tipo = campana.type
        ids_contactos_base_actual = campana.bd_contacto.contactos.values_list('id', flat=True)
        contactados = LlamadaLog.objects.filter(
            campana_id=campana.id,
            tipo_campana=campana_tipo,
            tipo_llamada=campana_tipo,
            contacto_id__in=ids_contactos_base_actual,
            event='CONNECT'
        ).values_list('contacto_id', flat=True)
        contactos_ids = set(ids_contactos_base_actual).difference(set(contactados))
        if len(contactos_ids) == 0:
            return
        filtro_contactos = "AND contacto_id in ('"
        filtro_contactos += "','".join([str(x) for x in contactos_ids])
        filtro_contactos += "')"
        params = {
            'campana_id': campana.id,
            'fecha_alta': campana.bd_contacto.fecha_alta,
            'tipo_campana': campana_tipo,
            'filtro_contactos': filtro_contactos,
        }
        logging.config.dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'queries': {'()': 'slowsql.LoggingFormatter', 'format': "text"},
            },
            'handlers': {
                'queries': {'class': 'logging.StreamHandler', 'formatter': 'queries'},
            },
            'loggers': {
                'django.db.backends': {'handlers': ['queries'], 'level': "DEBUG", 'propagate': False},
            },
        })
        if options['query']==1:
            self.query_1(params)
        else:
            self.query_2(params)

    def query_1(self, params):
        with connection.cursor() as cursor:
            sql = """
            SELECT r1.event, COUNT(r1.event)
                FROM "reportes_app_llamadalog" r1
                INNER JOIN (
                    SELECT contacto_id, MAX(id) AS id__max
                    FROM "reportes_app_llamadalog"
                    WHERE campana_id = {campana_id} AND
                        time >= '{fecha_alta}' AND
                        tipo_llamada = {tipo_campana} AND
                        tipo_campana = {tipo_campana} {filtro_contactos}
                    GROUP BY contacto_id
                ) r2
                ON r1.id = r2.id__max
                GROUP BY r1.event
            """.format(**params)
            cursor.execute(sql)

    def query_2(self, params):
        with connection.cursor() as cursor:
            sql = """
            SELECT event, COUNT(event)
                FROM "reportes_app_llamadalog"
                where id in (
                    SELECT MAX(id) AS id
                    FROM "reportes_app_llamadalog"
                    WHERE campana_id = {campana_id} AND
                        time >= '{fecha_alta}' AND
                        tipo_llamada = {tipo_campana} AND
                        tipo_campana = {tipo_campana} {filtro_contactos}
                    GROUP BY contacto_id
                )
                GROUP BY event
            """.format(**params)
            cursor.execute(sql)
