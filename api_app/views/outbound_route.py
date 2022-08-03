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
from django.utils.translation import ugettext as _
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from api_app.authentication import ExpiringTokenAuthentication
from api_app.views.permissions import TienePermisoOML
from api_app.serializers.outbound_route import (
    RutaSalienteSerializer,
    RutaSalienteTroncalSIPSerializer)
from configuracion_telefonia_app.models import RutaSaliente, TroncalSIP
from configuracion_telefonia_app.views.base import (
    eliminar_ruta_saliente_config)


class OutboundRouteList(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvieron las rutas entrantes '
                         'de forma exitosa'),
            'outboundRoutes': []}
        try:
            rutas_entrantes = RutaSaliente.objects.all().order_by('orden')
            data['outboundRoutes'] = [
                RutaSalienteSerializer(r).data for r in rutas_entrantes]
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al obtener las rutas salientes')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteCreate(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['post']

    def post(self, request):
        try:
            responseData = {
                'status': 'SUCCESS',
                'errors': {},
                'message': _('Se creo la ruta saliente '
                             'de forma exitosa')}
            ruta_saliente = RutaSalienteSerializer(data=request.data)
            if ruta_saliente.is_valid():
                ruta_saliente.save()
                return Response(data=responseData, status=status.HTTP_200_OK)
            else:
                responseData['status'] = 'ERROR'
                responseData['message'] = [
                    ruta_saliente.errors[key] for key in ruta_saliente.errors]
                responseData['errors'] = ruta_saliente.errors
                return Response(
                    data=responseData, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            responseData['status'] = 'ERROR'
            responseData['message'] = _('Error al crear la ruta saliente')
            return Response(
                data=responseData,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteUpdate(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['put']

    def put(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'errors': {},
            'message': _('Se actualizo la ruta saliente '
                         'de forma exitosa')}
        try:
            ruta_entrante = RutaSaliente.objects.get(pk=pk)
            serializer = RutaSalienteSerializer(
                ruta_entrante, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=data, status=status.HTTP_200_OK)
            else:
                data['status'] = 'ERROR'
                data['message'] = [
                    serializer.errors[key] for key in serializer.errors]
                data['errors'] = serializer.errors
                return Response(
                    data=data, status=status.HTTP_400_BAD_REQUEST)
        except RutaSaliente.DoesNotExist:
            data['status'] = 'ERROR'
            data['message'] = _('No existe la ruta saliente '
                                'que se quiere actualizar')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _('Error al actualizar '
                                'la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteDetail(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvo la informacion de la '
                         'ruta saliente de forma exitosa'),
            'outboundRoute': None}
        try:
            ruta_entrante = RutaSaliente.objects.get(pk=pk)
            data['outboundRoute'] = RutaSalienteSerializer(
                ruta_entrante).data
            return Response(data=data, status=status.HTTP_200_OK)
        except RutaSaliente.DoesNotExist:
            data['status'] = 'ERROR'
            data['message'] = _('No existe la ruta saliente '
                                'para obtener el detalle')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _('Error al obtener el detalle '
                                'de la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteDelete(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['delete']

    def delete(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se elimino la ruta saliente '
                         'de forma exitosa')}
        try:
            ruta_saliente = RutaSaliente.objects.get(pk=pk)
            if ruta_saliente.campana_set.exists():
                data['status'] = 'ERROR'
                data['message'] = _('No está permitido eliminar una '
                                    'ruta saliente asociada a una campaña')
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                eliminar_ruta_saliente_config(self, ruta_saliente)
                ruta_saliente.delete()
            return Response(data=data, status=status.HTTP_200_OK)
        except RutaSaliente.DoesNotExist:
            data['status'] = 'ERROR'
            data['message'] = _(u'No existe la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al eliminar la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteSIPTrunksList(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvieron las troncales sip '
                         'de forma exitosa'),
            'sipTrunks': []}
        try:
            troncales = TroncalSIP.objects.all().order_by('id')
            data['sipTrunks'] = [
                RutaSalienteTroncalSIPSerializer(t).data for t in troncales]
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al obtener las troncales')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OutboundRouteOrphanTrunks(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvieron las troncales huerfanas '
                         'de la ruta saliente de forma exitosa'),
            'orphanTrunks': []}
        try:
            ruta_saliente = RutaSaliente.objects.get(pk=pk)
            huerfanos = []
            for orden in ruta_saliente.secuencia_troncales.all():
                troncal = orden.troncal
                if troncal.ordenes_en_rutas_salientes.count() <= 1:
                    huerfanos.append(troncal)
            data['orphanTrunks'] = [
                RutaSalienteTroncalSIPSerializer(h).data for h in huerfanos]
            return Response(data=data, status=status.HTTP_200_OK)
        except RutaSaliente.DoesNotExist:
            data['status'] = 'ERROR'
            data['message'] = _(u'No existe la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al obtener las troncales huerfanas de la ruta saliente')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
