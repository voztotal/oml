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

import logging
from django.core.management.base import BaseCommand
from reportes_app.reportes.reporte_estadisticas_agentes import ReporteDiarioAgentesFamily


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Calcula y carga en Redis los datos del reporte de la actividad del dia actual de los agentes
    """

    help = 'Calcula y carga en Redis los datos del reporte diario de agentes.'

    def handle(self, *args, **options):
        family = ReporteDiarioAgentesFamily()
        try:
            family.regenerar_families()
        except Exception as e:
            logger.error('Fallo del comando: {0}'.format(e))
