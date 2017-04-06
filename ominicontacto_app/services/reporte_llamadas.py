# -*- coding: utf-8 -*-

import pygal
import datetime
import os

from pygal.style import Style, RedBlueStyle

from django.conf import settings
from django.db.models import Count
from ominicontacto_app.models import AgenteProfile, Queuelog
from ominicontacto_app.services.queue_log_service import QueueLogService

import logging as _logging

logger = _logging.getLogger(__name__)


ESTILO_AZUL_ROJO_AMARILLO = Style(
    background='transparent',
    plot_background='transparent',
    foreground='#555',
    foreground_light='#555',
    foreground_dark='#555',
    opacity='1',
    opacity_hover='.6',
    transition='400ms ease-in',
    colors=('#428bca', '#5cb85c', '#5bc0de', '#f0ad4e', '#d9534f',
            '#a95cb8', '#5cb8b5', '#caca43', '#96ac43', '#ca43ca')
)


class EstadisticasService():

    def _obtener_agentes(self):
        agentes = []
        for agente in Queuelog.objects.all().distinct('agent'):
            agentes.append(agente.agent)
        return agentes

    def calcular_tiempo_sesion(self, agentes, fecha_inferior, fecha_superior):

        eventos_sesion = ['ADDMEMBER', 'REMOVEMEMBER']

        if fecha_inferior and fecha_superior:
            fecha_desde = datetime.datetime.combine(fecha_inferior,
                                                    datetime.time.min)
            fecha_hasta = datetime.datetime.combine(fecha_superior,
                                                    datetime.time.max)

        logs_queue = Queuelog.objects.filter(
            queuename='ALL',
            event__in=eventos_sesion,
            time__range=(fecha_desde, fecha_hasta)).order_by('-time')

        agentes_tiempo = []
        print logs_queue
        print agentes
        for agente in agentes:
            tiempo_agente = []
            logs_time = logs_queue.filter(agent=agente)
            print logs_time
            is_remove = False
            time_actual = None
            for logs in logs_time:
                if is_remove and logs.event == 'ADDMEMBER':
                    resta = time_actual - logs.time
                    print resta
                    tiempo_agente.append(agente)
                    tiempo_agente.append(logs.time.strftime('%Y-%m-%d'))
                    tiempo_string = str(resta) + "hs"
                    tiempo_agente.append(str(tiempo_string))
                    agentes_tiempo.append(tiempo_agente)
                    tiempo_agente = []
                    is_remove = False
                    time_actual = None
                if logs.event == 'REMOVEMEMBER':
                    time_actual = logs.time
                    is_remove = True
        print agentes_tiempo
        return agentes_tiempo

    def calcular_tiempo_pausa(self, agentes, fecha_inferior, fecha_superior):

        eventos_sesion = ['PAUSEALL', 'UNPAUSEALL']

        if fecha_inferior and fecha_superior:
            fecha_desde = datetime.datetime.combine(fecha_inferior,
                                                    datetime.time.min)
            fecha_hasta = datetime.datetime.combine(fecha_superior,
                                                    datetime.time.max)

        logs_queue = Queuelog.objects.filter(
            queuename='ALL',
            event__in=eventos_sesion,
            time__range=(fecha_desde, fecha_hasta)).order_by('-time')

        agentes_tiempo = []

        for agente in agentes:
            tiempo_agente = []
            logs_time = logs_queue.filter(agent=agente)
            is_unpause = False
            time_actual = None
            for logs in logs_time:
                if is_unpause and logs.event == 'PAUSEALL':
                    resta = time_actual - logs.time
                    tiempo_agente.append(agente)
                    tiempo_agente.append(logs.time.strftime('%Y-%m-%d'))
                    tiempo_string = str(resta) + "hs"
                    tiempo_agente.append(str(tiempo_string))
                    tiempo_agente.append(logs.data1)
                    agentes_tiempo.append(tiempo_agente)
                    tiempo_agente = []
                    is_unpause = False
                    time_actual = None
                if logs.event == 'UNPAUSEALL':
                    time_actual = logs.time
                    is_unpause = True
        return agentes_tiempo

    def calcular_tiempo_llamada(self, agentes, fecha_inferior, fecha_superior):

        eventos_sesion = ['COMPLETECALLER', 'COMPLETEAGENT']

        if fecha_inferior and fecha_superior:
            fecha_desde = datetime.datetime.combine(fecha_inferior,
                                                    datetime.time.min)
            fecha_hasta = datetime.datetime.combine(fecha_superior,
                                                    datetime.time.max)

        logs_queue = Queuelog.objects.filter(
            event__in=eventos_sesion,
            time__range=(fecha_desde, fecha_hasta)).order_by('-time')

        agentes_tiempo = []

        for agente in agentes:
            tiempo_agente = []
            logs_agentes = logs_queue.filter(agent=agente)
            tiempo_agente.append(agente)
            lista_tiempo_llamada = [int(log.data2) for log in logs_agentes]
            tiempo_agente.append(sum(lista_tiempo_llamada))
            agentes_tiempo.append(tiempo_agente)
            tiempo_agente = []

        return agentes_tiempo


    def _calcular_estadisticas(self, fecha_inferior, fecha_superior):
        agentes = self._obtener_agentes()
        agentes_tiempo = self.calcular_tiempo_sesion(agentes, fecha_inferior,
                                                     fecha_superior)
        agentes_pausa = self.calcular_tiempo_pausa(agentes, fecha_inferior,
                                                   fecha_superior)
        agentes_llamadas = self.calcular_tiempo_llamada(agentes,
                                                        fecha_inferior, fecha_superior)
        dic_estadisticas = {
            'agentes_tiempo': agentes_tiempo,
            'agentes_pausa': agentes_pausa,
            'agentes_llamadas': agentes_llamadas

        }
        return dic_estadisticas

    def general_campana(self, fecha_inferior, fecha_superior):
        estadisticas = self._calcular_estadisticas(fecha_inferior,
                                                   fecha_superior)

        if estadisticas:
            logger.info("Generando grafico calificaciones de campana por cliente ")

        return estadisticas



        # # Barra: Total de llamados atendidos en cada intento por campana.
        # barra_campana_calificacion = pygal.Bar(  # @UndefinedVariable
        #     show_legend=False,
        #     style=ESTILO_AZUL_ROJO_AMARILLO)
        # barra_campana_calificacion.title = 'Cantidad de calificacion de cliente '
        #
        # barra_campana_calificacion.x_labels = \
        #     estadisticas['calificaciones_nombre']
        # barra_campana_calificacion.add('cantidad',
        #                                estadisticas['calificaciones_cantidad'])
        # barra_campana_calificacion.render_to_png(os.path.join(settings.MEDIA_ROOT,
        #     "reporte_campana", "barra_campana_calificacion.png"))
        #
        # # Barra: Total de llamados no atendidos en cada intento por campana.
        # barra_campana_no_atendido = pygal.Bar(  # @UndefinedVariable
        #     show_legend=False,
        #     style=ESTILO_AZUL_ROJO_AMARILLO)
        # barra_campana_no_atendido.title = 'Cantidad de llamadas no atendidos '
        #
        # barra_campana_no_atendido.x_labels = \
        #     estadisticas['resultado_nombre']
        # barra_campana_no_atendido.add('cantidad',
        #                               estadisticas['resultado_cantidad'])
        # barra_campana_no_atendido.render_to_png(
        #     os.path.join(settings.MEDIA_ROOT,
        #                  "reporte_campana", "barra_campana_no_atendido.png"))
        #
        # return {
        #     'estadisticas': estadisticas,
        #     'barra_campana_calificacion': barra_campana_calificacion,
        #     'dict_campana_counter': zip(estadisticas['calificaciones_nombre'],
        #                                 estadisticas['calificaciones_cantidad'])
        #     ,
        #     'total_asignados': estadisticas['total_asignados'],
        #     'agentes_venta': estadisticas['agentes_venta'],
        #     'total_calificados': estadisticas['total_calificados'],
        #     'total_ventas': estadisticas['total_ventas'],
        #     'barra_campana_no_atendido': barra_campana_no_atendido,
        #     'dict_no_atendido_counter': zip(estadisticas['resultado_nombre'],
        #                                     estadisticas['resultado_cantidad']),
        #     'total_no_atendidos': estadisticas['total_no_atendidos'],
        #     'calificaciones': estadisticas['calificaciones']
        # }
