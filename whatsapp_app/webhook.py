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

from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from whatsapp_app.models import Linea


class WebhookView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, identificador):
        try:
            mode = request.GET.get("hub.mode", None)
            token = request.GET.get("hub.verify_token", None)
            challenge = request.GET.get("hub.challenge", None)
            # Check if a token and mode were sent
            line_token = Linea.objects.filter(identificador=identificador).first().token_validacion
            if mode and token == token:
                # Check the mode and token sent are correct
                if mode == "subscribe" and token == line_token:
                    return HttpResponse(challenge, status=status.HTTP_200_OK)
            return HttpResponse(challenge, status=status.HTTP_403_FORBIDDEN)
        except Exception:
            return HttpResponse(challenge, status=status.HTTP_403_FORBIDDEN)

    def post(self, request, identificador):
        if request.body:
            body = json.loads(request.body)
            identificador = Linea.objects.get(identificador=identificador).proveedor.identificador
            if body["entry"][0]["id"] == identificador:
                if "contacts" in body["entry"][0]["changes"][0]["value"]:
                    cliente = body["entry"][0]["changes"][0]["value"]["contacts"][0]["wa_id"]
                    type = body["entry"][0]["changes"][0]["value"]["messages"][0]["type"]
                    mensaje = body["entry"][0]["changes"][0]["value"]["messages"][0][type]
                    print(cliente, ": ", mensaje)
                else:
                    recipient_id =\
                        body["entry"][0]["changes"][0]["value"]["statuses"][0]["recipient_id"]
                    status_mensaje =\
                        body["entry"][0]["changes"][0]["value"]["statuses"][0]["status"]
                    print(recipient_id, status_mensaje)
                return HttpResponse("OK", status=status.HTTP_200_OK)
        return HttpResponse("OK", status=status.HTTP_403_FORBIDDEN)
