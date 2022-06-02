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

from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api_app.views.permissions import TienePermisoOML
from api_app.authentication import ExpiringTokenAuthentication
from api_app.serializers import AudioSerializer

from ominicontacto_app.models import ArchivoDeAudio
from configuracion_telefonia_app.models import Playlist


class ListadoAudiosView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (TienePermisoOML, )
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication, )
    serializer_class = AudioSerializer

    def get_queryset(self):
        return ArchivoDeAudio \
            .objects \
            .all() \
            .exclude(borrado=True)


class SavePlaylistOrder(APIView):
    """ Guarda un nuevo orden para las musicas de una playlist """
    permission_classes = (TienePermisoOML, )
    authentication_classes = (SessionAuthentication, ExpiringTokenAuthentication, )
    renderer_classes = (JSONRenderer, )
    http_method_names = ['post']

    def post(self, request):
        playlist_id = request.POST.get('id', 0)
        try:
            playlist = Playlist.objects.get(id=playlist_id)
        except Playlist.DoesNotExist:
            return Response(data={
                'status': 'ERROR',
                'message': _('Playlist inexistente')
            })

        orden = request.POST.getlist('order[]', [])
        ids_musicas = set([str(x) for x in playlist.musicas.values_list('id', flat=True)])
        if not ids_musicas == set(orden):
            return Response(data={
                'status': 'ERROR',
                'message': _('IDs de musicas incorrectos: {0}' + str(orden))
            })

        for musica in playlist.musicas.all():
            musica.orden = orden.index(str(musica.id))
            musica.save()

        return Response(data={
            'status': 'OK',
        })
        # TODO: IMPACTAR EN REDIS? / ASTERISK?
