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
from django.forms import ValidationError
from django.utils.translation import ugettext as _
from configuracion_telefonia_app.regeneracion_configuracion_telefonia import (
    RestablecerConfiguracionTelefonicaError,
    SincronizadorDeConfiguracionPausaAsterisk)
from ominicontacto_app.utiles import validar_nombres_campanas
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication
from api_app.authentication import ExpiringTokenAuthentication
from api_app.views.permissions import TienePermisoOML
from api_app.serializers import (
    PausaSerializer)
from ominicontacto_app.models import Pausa


class PauseList(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvieron las pausas '
                         'de forma exitosa'),
            'pauses': []}
        try:
            pausas = Pausa.objects.all().order_by('id')
            data['pauses'] = [
                PausaSerializer(p).data for p in pausas]
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al obtener las pausas')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseCreate(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['post']

    def post(self, request):
        try:
            responseData = {
                'status': 'SUCCESS',
                'message': _('Se creo la pausa '
                             'de forma exitosa')}
            validar_nombres_campanas(request.data['nombre'])
            pausa = PausaSerializer(data=request.data)
            if pausa.is_valid():
                pausa.save()
                return Response(data=responseData, status=status.HTTP_200_OK)
            else:
                responseData['status'] = 'ERROR'
                responseData['message'] = [
                    pausa.errors[key] for key in pausa.errors]
                responseData['errors'] = pausa.errors
                return Response(
                    data=responseData, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as ve:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': ve
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            responseData['status'] = 'ERROR'
            responseData['message'] = _('Error al crear la pausa')
            return Response(
                data=responseData,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseUpdate(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['put']

    def put(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'errors': {},
            'message': _('Se actualizo la pausa '
                         'de forma exitosa')}
        try:
            validar_nombres_campanas(request.data['nombre'])
            pausa = Pausa.objects.get(pk=pk)
            serializer = PausaSerializer(
                pausa, data=request.data)
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
        except Pausa.DoesNotExist:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': 'No existe la pausa'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as ve:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': ve
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _('Error al actualizar '
                                'la pausa')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseDelete(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['delete']

    def delete(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se elimino la pausa '
                         'de forma exitosa')}
        try:
            pausa = Pausa.objects.get(pk=pk)
            if pausa.tiene_configuraciones():
                data['status'] = 'ERROR'
                data['message'] = _('No está permitido eliminar un '
                                    'pausa con configuraciones creadas')
                return Response(
                    data=data, status=status.HTTP_400_BAD_REQUEST)
            else:
                pausa.eliminada = True
                pausa.save()
                try:
                    sincronizador = SincronizadorDeConfiguracionPausaAsterisk()
                    sincronizador.eliminar_y_regenerar_asterisk(pausa)
                    return Response(data=data, status=status.HTTP_200_OK)
                except RestablecerConfiguracionTelefonicaError as e:
                    print("Operación Errónea! "
                          "No se realizo de manera correcta "
                          "la sincronización de los datos en asterisk "
                          "según el siguiente error: {0}".format(e))
                    data['status'] = 'ERROR'
                    data['message'] = _('Error al sincronizar '
                                        'la pausa con asterisk')
                    return Response(
                        data=data,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Pausa.DoesNotExist:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': 'No existe la pausa'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al eliminar la pausa')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseReactivate(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['put']

    def put(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se reactivo la pausa '
                         'de forma exitosa')}
        try:
            pausa = Pausa.objects.get(pk=pk)
            pausa.eliminada = False
            pausa.save()
            try:
                sincronizador = SincronizadorDeConfiguracionPausaAsterisk()
                sincronizador.regenerar_asterisk(pausa)
                return Response(data=data, status=status.HTTP_200_OK)
            except RestablecerConfiguracionTelefonicaError as e:
                print("Operación Errónea! "
                      "No se realizo de manera correcta "
                      "la sincronización de los datos en asterisk "
                      "según el siguiente error: {0}".format(e))
                data['status'] = 'ERROR'
                data['message'] = _(u'Error al sincronizar pausa con asterisk')
                return Response(
                    data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Pausa.DoesNotExist:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': 'No existe la pausa'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _(u'Error al reactivar la pausa')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PauseDetail(APIView):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (
        SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['get']

    def get(self, request, pk):
        data = {
            'status': 'SUCCESS',
            'message': _('Se obtuvo la informacion de la '
                         'pausa de forma exitosa'),
            'pause': None}
        try:
            pausa = Pausa.objects.get(pk=pk)
            data['pause'] = PausaSerializer(pausa).data
            return Response(data=data, status=status.HTTP_200_OK)
        except Pausa.DoesNotExist:
            return Response(
                data={
                    'status': 'ERROR',
                    'message': 'No existe la pausa'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception:
            data['status'] = 'ERROR'
            data['message'] = _('Error al obtener el detalle '
                                'de la pausa')
            return Response(
                data=data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
