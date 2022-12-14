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

import whatsapp_app.api.v1.proveedor
import whatsapp_app.api.v1.linea
import whatsapp_app.api.v1.destinos

from whatsapp_app.api import ViewSetRouter

router = ViewSetRouter(trailing_slash=False)

routes = (
    (r"providers", whatsapp_app.api.v1.proveedor.ViewSet),
    (r"lines", whatsapp_app.api.v1.linea.ViewSet),
    (r"destinos", whatsapp_app.api.v1.destinos.ViewSet),
)

for route in routes:
    router.register(*route)

api_urls_v1 = router.urls
