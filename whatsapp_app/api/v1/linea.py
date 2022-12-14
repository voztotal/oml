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

# APIs para visualizar lineas
from django.utils.translation import ugettext as _
from django.contrib.postgres.fields import JSONField
from django.utils.functional import cached_property
from django.db.models import F
from django.db.models import Func
from django.db.models import Value
from rest_framework import serializers
from rest_framework import response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from api_app.views.permissions import TienePermisoOML
from api_app.authentication import ExpiringTokenAuthentication
from whatsapp_app.api.utils import HttpResponseStatus, get_response_data

from whatsapp_app.models import Linea


class ListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    proveedor = serializers.CharField(source='proveedor.id')
    numero = serializers.CharField()
    identificador = serializers.CharField()
    token_validacion = serializers.CharField()
    destino = serializers.CharField(source='destino.nombre', required=False)
    mensaje_bienvenida = serializers.CharField()
    mensaje_despedida = serializers.CharField()


class CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Linea
        fields = [
            'id',
            'nombre',
            'proveedor',
            'numero',
            'identificador',
            'token_validacion',
            'destino',
            'mensaje_bienvenida',
            'mensaje_despedida',
        ]


class RetrieveSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    proveedor = serializers.CharField(source='proveedor.id')
    numero = serializers.CharField()
    identificador = serializers.CharField()
    token_validacion = serializers.CharField()
    destino = serializers.CharField(source='destino.id')
    mensaje_bienvenida = serializers.CharField()
    mensaje_despedida = serializers.CharField()


class UpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Linea
        fields = [
            'id',
            'nombre',
            'proveedor',
            'numero',
            'identificador',
            'token_validacion',
            'destino',
            'mensaje_bienvenida',
            'mensaje_despedida',
        ]

    @cached_property
    def _readable_fields(self):
        return [f for f in self.fields.values()
                if not f.write_only and f.field_name in self.initial_data]


class ViewSet(viewsets.ViewSet):
    permission_classes = [TienePermisoOML]
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication, )

    def list(self, request):
        try:
            queryset = Linea.objects.filter(
                is_active=True
            ).annotate(
                created_jsonb=Func(
                    Value("date"),
                    Func(F("created_at"), Value("YYYY-MM-DD"), function="to_char"),
                    Value("user"),
                    F("created_by__username"),
                    function="jsonb_build_object",
                    output_field=JSONField(),
                ),
                updated_jsonb=Func(
                    Value("date"),
                    Func(F("updated_at"), Value("YYYY-MM-DD"), function="to_char"),
                    Value("user"),
                    F("updated_by__username"),
                    function="jsonb_build_object",
                    output_field=JSONField(),
                ),
            ).order_by(
                "nombre",
            )
            serializer = ListSerializer(queryset, many=True)
            return response.Response(
                data=get_response_data(
                    status=HttpResponseStatus.SUCCESS,
                    message=_('Se obtuvieron las líneas de forma exitosa'),
                    data=serializer.data),
                status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return response.Response(
                data=get_response_data(
                    message=_('Error al obtener las líneas')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        try:
            serializer = CreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(
                    created_by=request.user,
                    updated_by=request.user,
                )
                return response.Response(
                    data=get_response_data(
                        status=HttpResponseStatus.SUCCESS,
                        message=_('Se creo la línea de forma exitosa'),
                        data=serializer.data),
                    status=status.HTTP_201_CREATED)
            else:
                return response.Response(
                    data=get_response_data(
                        message=_('Error en los datos'), errors=serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return response.Response(
                data=get_response_data(message=_('Error al crear la línea')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk):
        try:
            queryset = Linea.objects.filter(
                is_active=True
            ).annotate(
                created_jsonb=Func(
                    Value("date"),
                    Func(F("created_at"), Value("YYYY-MM-DD"), function="to_char"),
                    Value("user"),
                    F("created_by__username"),
                    function="jsonb_build_object",
                    output_field=JSONField(),
                ),
                updated_jsonb=Func(
                    Value("date"),
                    Func(F("updated_at"), Value("YYYY-MM-DD"), function="to_char"),
                    Value("user"),
                    F("updated_by__username"),
                    function="jsonb_build_object",
                    output_field=JSONField(),
                ),
            )
            instance = queryset.get(pk=pk)
            serializer = RetrieveSerializer(instance)
            return response.Response(
                data=get_response_data(
                    status=HttpResponseStatus.SUCCESS,
                    data=serializer.data,
                    message=_('Se obtuvo la línea de forma exitosa')),
                status=status.HTTP_200_OK)
        except Linea.DoesNotExist:
            return response.Response(
                data=get_response_data(message=_('Línea no encontrada')),
                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(e)
            return response.Response(
                data=get_response_data(
                    message=_('Error al obtener la línea')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        try:
            queryset = Linea.objects.filter(is_active=True)
            instance = queryset.get(pk=pk)
            serializer = UpdateSerializer(instance, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(updated_by=request.user)
                return response.Response(
                    data=get_response_data(
                        status=HttpResponseStatus.SUCCESS,
                        data=serializer.data,
                        message=_('Se actualizó la línea de forma exitosa')),
                    status=status.HTTP_200_OK)
            else:
                return response.Response(
                    data=get_response_data(
                        message=_('Error en los datos'), errors=serializer.errors),
                    status=status.HTTP_400_BAD_REQUEST)
        except Linea.DoesNotExist:
            return response.Response(
                data=get_response_data(message=_('Línea no encontrada')),
                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return response.Response(
                data=get_response_data(
                    message=_('Error al actualizar la línea')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        try:
            queryset = Linea.objects.filter(is_active=True)
            instance = queryset.get(pk=pk)
            instance.delete()
            return response.Response(
                data=get_response_data(
                    status=HttpResponseStatus.SUCCESS,
                    message=_('Se elimino la línea de forma exitosa')),
                status=status.HTTP_200_OK)
        except Linea.DoesNotExist:
            return response.Response(
                data=get_response_data(message=_('Línea no encontrado')),
                status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return response.Response(
                data=get_response_data(
                    message=_('Error al eliminar la línea')),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
