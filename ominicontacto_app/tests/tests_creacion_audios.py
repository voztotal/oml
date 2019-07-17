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

from django.test import TestCase

from factory import django as factory_django

from ominicontacto_app.forms import ArchivoDeAudioForm
from ominicontacto_app.tests.factories import ArchivoDeAudioFactory


class CreacionAudioTests(TestCase):

    def test_audios_no_permitidos_vista_creacion_audios(self):
        audio_no_permitido = ArchivoDeAudioFactory(
            audio_original=factory_django.FileField(filename='test.ogg'))
        audio_form = ArchivoDeAudioForm({
            'audio_original': audio_no_permitido.audio_original.file,
            'descripcion': 'audio_no_permitido'
        }, instance=audio_no_permitido)
        self.assertFalse(audio_form.is_valid())
        self.assertEqual(
            audio_form.errors['__all__'], [u'Archivos permitidos: .wav, .mp3'])
