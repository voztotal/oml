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
import json
from functools import reduce
from operator import or_
from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import decorators
from rest_framework.authentication import SessionAuthentication
from api_app.views.permissions import TienePermisoOML
from api_app.authentication import ExpiringTokenAuthentication
from whatsapp_app.api.utils import HttpResponseStatus, get_response_data

from ominicontacto_app.models import Campana, Contacto


class ListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    phone = serializers.CharField(source='telefono')
    data = serializers.CharField(source='datos')


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = [
            'id',
            'telefono',
            'datos',
            'bd_contacto',
        ]


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = [
            'id',
            'telefono',
            'datos',
            'bd_contacto',
        ]


class ViewSet(viewsets.ViewSet):
    permission_classes = [TienePermisoOML]
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication, )

    def list(self, request, campana_pk):
        try:
            filtro = request.GET.get('search')
            campana = Campana.objects.get(id=campana_pk)
            listado_de_contacto = Contacto.objects.\
                contactos_by_filtro_bd_contacto(campana.bd_contacto, filtro)
        except Exception:
            listado_de_contacto = Contacto.objects.contactos_by_bd_contacto(
                campana.bd_contacto)
        serializer = ListSerializer(listado_de_contacto, many=True)
        return response.Response(
            data=get_response_data(
                status=HttpResponseStatus.SUCCESS,
                message=_('Se obtuvieron las contactos de forma exitosa'),
                data=serializer.data),
            status=status.HTTP_200_OK)

    def create(self, request, campana_pk):
        try:
            campana = Campana.objects.get(id=campana_pk)
            bd_contacto = campana.bd_contacto
            campos_bd = json.loads(bd_contacto.metadata)['nombres_de_columnas']
            if set(request.data.keys()).issubset(set(campos_bd)):
                data = {
                    "telefono": request.data.pop('telefono'),  # requerido
                    "bd_contacto": bd_contacto.id,
                    "datos": str(list(request.data.values()))
                }
                serializer = CreateSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(
                        data=get_response_data(
                            status=HttpResponseStatus.SUCCESS,
                            message=_('Se creo el nuevo contacto de forma exitosa'),
                            data=serializer.data),
                        status=status.HTTP_201_CREATED)
            return response.Response(
                data=get_response_data(
                    message=_('Error en los datos'), errors=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return response.Response(
                data=get_response_data(message=_('Error al crear el contacto')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, campana_pk, pk):
        try:
            campana = Campana.objects.get(id=campana_pk)
            bd_contacto = campana.bd_contacto
            campos_bd = json.loads(bd_contacto.metadata)['nombres_de_columnas']
            if set(request.data.keys()).issubset(set(campos_bd)):
                if "telefono" in request.data:
                    data = {
                        "telefono": request.data.pop('telefono'),
                        "datos": str(list(request.data.values()))
                    }
                else:
                    data = {
                        "datos": str(list(request.data.values()))
                    }
                instance = Contacto.objects.get(pk=pk)
                serializer = UpdateSerializer(instance, data=data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return response.Response(
                        data=get_response_data(
                            status=HttpResponseStatus.SUCCESS,
                            message=_('Se actualizo el nuevo contacto de forma exitosa'),
                            data=serializer.data),
                        status=status.HTTP_201_CREATED)

            return response.Response(
                data=get_response_data(
                    status=status.HTTP_400_BAD_REQUEST,
                    message=_('Error en los datos')))

        except Contacto.DoesNotExist:
            return response.Response(
                data=get_response_data(message=_('Contacto no encontrado')),
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return response.Response(
                data=get_response_data(
                    message=_('Error al actualizar el contacto')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.action(detail=False, methods=["get"])
    def db_fields(self, request, campana_pk):
        try:
            campana = Campana.objects.get(id=campana_pk)
            columnas = json.loads(campana.bd_contacto.metadata)
            data = []
            for index, name in enumerate(columnas['nombres_de_columnas'], start=0):
                field = {}
                field['name'] = name
                field['required'] = name in campana.get_campos_obligatorios()
                field['is_phone_field'] = index in columnas['cols_telefono']
                data.append(field)
            return response.Response(
                data=get_response_data(
                    status=HttpResponseStatus.SUCCESS,
                    data=data),
                status=status.HTTP_200_OK)
        except Exception:
            return response.Response(
                data=get_response_data(
                    message=_('Error al obtener los campos de contacto')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @decorators.action(detail=False, methods=["post"])
    def search(self, request, campana_pk):
        try:
            values = request.data.values()
            q_list = [Q(datos__contains=x) for x in values]
            if 'dial_code' in request.data:
                q_list.append(Q(telefono__contains=request.data['dial_code']))
            if 'phone' in request.data:
                q_list.append(Q(telefono=request.data['phone']))
            campana = Campana.objects.get(id=campana_pk)
            contactos = Contacto.objects.filter(
                reduce(or_, q_list), bd_contacto=campana.bd_contacto)
            serializer = ListSerializer(contactos, many=True)
            return response.Response(
                data=get_response_data(
                    status=HttpResponseStatus.SUCCESS,
                    data=serializer.data),
                status=status.HTTP_200_OK)
        except Exception:
            return response.Response(
                data=get_response_data(
                    message=_('Error al obtener contactos')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
