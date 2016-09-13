# -*- coding: utf-8 -*-


from django.conf import settings
from django.views.generic import FormView, ListView
from ominicontacto_app.forms import (
    GrabacionBusquedaForm
)
from ominicontacto_app.models import (
    Grabacion
)
from ominicontacto_app.services.reporte_grafico import GraficoService


class BusquedaGrabacionFormView(FormView):
    form_class = GrabacionBusquedaForm
    template_name = 'busqueda_grabacion.html'

    def get_context_data(self, **kwargs):
        context = super(BusquedaGrabacionFormView, self).get_context_data(
            **kwargs)
        context['grabacion_url'] = settings.OML_GRABACIONES_URL
        return context

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(
            listado_de_grabaciones=Grabacion.objects.all()))

    def form_valid(self, form):
        fecha = form.cleaned_data.get('fecha')
        tipo_llamada = form.cleaned_data.get('tipo_llamada')
        id_cliente = form.cleaned_data.get('id_cliente')
        tel_cliente = form.cleaned_data.get('tel_cliente')
        sip_agente = form.cleaned_data.get('sip_agente')
        campana = form.cleaned_data.get('campana')
        listado_de_grabaciones = Grabacion.objects.grabacion_by_filtro(fecha,
            tipo_llamada, id_cliente, tel_cliente, sip_agente, campana)
        return self.render_to_response(self.get_context_data(
            listado_de_grabaciones=listado_de_grabaciones))


class GrabacionReporteListView(ListView):
    """
    Esta vista lista los objetos Capanas
    diferenciadas por sus estados actuales.
    Pasa un diccionario al template
    con las claves como estados.
    """

    template_name = 'grabaciones/total_llamadas.html'
    context_object_name = 'grabaciones'
    model = Grabacion

    def get_context_data(self, **kwargs):
        context = super(GrabacionReporteListView, self).get_context_data(
           **kwargs)

        # obtener_estadisticas_render_graficos_supervision()
        service = GraficoService()
        context['graficos_estadisticas'] = service.general_llamadas_hoy()
        return context

