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

import logging


from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.views.generic import UpdateView

from configuracion_telefonia_app.models import AmdConf, EsquemaGrabaciones
from configuracion_telefonia_app.forms import AmdConfForm, EsquemaGrabacionesForm

from configuracion_telefonia_app.regeneracion_configuracion_telefonia import \
    SincronizadorDeConfiguracionAmdConfAsterisk, SincronizadorDeEsquemaGrabacionesAsterisk


logger = logging.getLogger(__name__)


class ConfiguracionAMDUpdateView(UpdateView):
    """Vista que permite editar el modulo AMD de Asterisk"""
    model = AmdConf
    form_class = AmdConfForm
    template_name = 'editar_configuracion_amd.html'
    message = _('Se ha modificado la configuración AMD del sistema con éxito')

    def get_success_url(self):
        return reverse('ajustar_configuracion_amd', args=(1,))

    def form_valid(self, form):
        response = super(ConfiguracionAMDUpdateView, self).form_valid(form)
        sincronizador = SincronizadorDeConfiguracionAmdConfAsterisk()
        sincronizador.regenerar_asterisk()
        messages.add_message(self.request, messages.SUCCESS, self.message)
        return response


class EsquemaGrabacionesUpdateView(UpdateView):
    """Vista que permite definir el formato que tendran los nombres de
    archivos de grabaciones
    """
    model = EsquemaGrabaciones
    form_class = EsquemaGrabacionesForm
    template_name = 'editar_esquema_grabacion.html'
    message = _('Se ha modificado el formato de los nombres de graciones con éxito')

    def get_success_url(self):
        return reverse('ajustar_formato_grabaciones', args=(1,))

    def form_valid(self, form):
        response = super(EsquemaGrabacionesUpdateView, self).form_valid(form)
        sincronizador = SincronizadorDeEsquemaGrabacionesAsterisk()
        sincronizador.regenerar_asterisk()
        messages.add_message(self.request, messages.SUCCESS, self.message)
        return response
