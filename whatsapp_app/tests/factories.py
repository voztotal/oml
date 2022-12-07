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
import faker
import string
from factory import (DjangoModelFactory, fuzzy, lazy_attribute, Sequence, SubFactory)

from ominicontacto_app.tests.factories import UserFactory
from whatsapp_app.models import ConfiguracionProveedor


faker = faker.Factory.create()


class ConfiguracionProveedorFactory(DjangoModelFactory):
    class Meta:
        model = ConfiguracionProveedor
    nombre = Sequence(lambda n: "proveedor_{0}".format(n))
    tipo_proveedor = lazy_attribute(lambda a: faker.random_number(3))
    identificador = fuzzy.FuzzyText(length=12, chars=string.ascii_uppercase + string.digits)
    token_autorizacion = fuzzy.FuzzyText(length=12, chars=string.ascii_uppercase + string.digits)
    created_by = SubFactory(UserFactory)
    updated_by = SubFactory(UserFactory)
