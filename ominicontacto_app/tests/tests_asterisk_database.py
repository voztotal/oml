# -*- coding: utf-8 -*-

"""
Tests del metodo 'ominicontacto_app.services.asterisk_database'
"""

from __future__ import unicode_literals


from ominicontacto_app.tests.utiles import OMLBaseTest
from ominicontacto_app.services.asterisk_database import (
    CampanaFamily, AgenteFamily, RutaSalienteFamily, TrunkFamily
)
from ominicontacto_app.utiles import elimina_espacios
from configuracion_telefonia_app.tests.factories import (
    TroncalSIPFactory, RutaSalienteFactory, PatronDeDiscadoFactory)


class AsteriskDatabaseTest(OMLBaseTest):

    def setUp(self):
        self.campana_dialer = self.crear_campana_dialer()
        self.campana_entrante = self.crear_campana_entrante()
        user = self.crear_user_agente()
        self.agente = self.crear_agente_profile(user)

    def test_devuelve_correctamente_dict_campana_asterisk(self):
        """
        este test testea el diccionario de la family de la campana
        """
        servicio = CampanaFamily()
        dict_campana = servicio.create_dict(self.campana_entrante)

        keys_asterisk = ['QNAME', 'TYPE', 'REC', 'AMD', 'CALLAGENTACTION',
                         'RINGTIME', 'QUEUETIME', 'MAXQCALLS', 'SL', 'TC',
                         'IDJSON', 'PERMITOCCULT', 'MAXCALLS', 'FAILOVER']
        for key in keys_asterisk:
            self.assertIn(key, dict_campana.keys())

    def test_falla_key_dict_campana_asterisk(self):
        """
        este test testea el diccionario de la family de la campana y
         no encuentra key
        """
        servicio = CampanaFamily()
        dict_campana = servicio.create_dict(self.campana_entrante)

        self.assertNotIn('WAITTIME', dict_campana.keys())

        self.assertNotIn('DELAY', dict_campana.keys())

    def test_devuelve_correctamente_values_campana_entrante_asterisk(self):
        """
        este test testea los values del diccionario de la family de la campana
        entrante
        """
        servicio = CampanaFamily()
        dict_campana = servicio.create_dict(self.campana_entrante)

        nombre_campana = "{0}_{1}".format(self.campana_entrante.id,
                                          elimina_espacios(self.campana_entrante.nombre))
        self.assertEqual(dict_campana['QNAME'], nombre_campana)
        self.assertEqual(dict_campana['TYPE'], self.campana_entrante.type)
        self.assertEqual(dict_campana['REC'], self.campana_entrante.queue_campana.auto_grabacion)
        self.assertEqual(dict_campana['AMD'],
                         self.campana_entrante.queue_campana.detectar_contestadores)
        self.assertEqual(dict_campana['CALLAGENTACTION'], self.campana_entrante.tipo_interaccion)
        self.assertEqual(dict_campana['RINGTIME'], self.campana_entrante.queue_campana.timeout)
        self.assertEqual(dict_campana['QUEUETIME'], self.campana_entrante.queue_campana.wait)
        self.assertEqual(dict_campana['MAXQCALLS'], self.campana_entrante.queue_campana.maxlen)
        self.assertEqual(dict_campana['SL'], self.campana_entrante.queue_campana.servicelevel)
        audio = "oml/{0}".format(
            self.campana_entrante.queue_campana.audio_de_ingreso.get_filename_audio_asterisk())
        self.assertEqual(dict_campana['WELCOMEPLAY'], audio)
        self.assertEqual(dict_campana['TC'], "")
        self.assertEqual(dict_campana['IDJSON'], "")
        self.assertEqual(dict_campana['PERMITOCCULT'], "")
        self.assertEqual(dict_campana['MAXCALLS'], "")
        self.assertEqual(dict_campana['FAILOVER'], "")

    def test_devuelve_correctamente_values_campana_dialer_asterisk(self):
        """
        este test testea los values del diccionario de la family de la campana
        dialer
        """
        servicio = CampanaFamily()
        dict_campana = servicio.create_dict(self.campana_dialer)

        nombre_campana = "{0}_{1}".format(self.campana_dialer.id,
                                          elimina_espacios(self.campana_dialer.nombre))
        self.assertEqual(dict_campana['QNAME'], nombre_campana)
        self.assertEqual(dict_campana['TYPE'], self.campana_dialer.type)
        self.assertEqual(dict_campana['REC'], self.campana_dialer.queue_campana.auto_grabacion)
        self.assertEqual(dict_campana['AMD'],
                         self.campana_dialer.queue_campana.detectar_contestadores)
        self.assertEqual(dict_campana['CALLAGENTACTION'], self.campana_dialer.tipo_interaccion)
        self.assertEqual(dict_campana['RINGTIME'], self.campana_dialer.queue_campana.timeout)
        self.assertEqual(dict_campana['QUEUETIME'], self.campana_dialer.queue_campana.wait)
        self.assertEqual(dict_campana['MAXQCALLS'], self.campana_dialer.queue_campana.maxlen)
        self.assertEqual(dict_campana['SL'], self.campana_dialer.queue_campana.servicelevel)
        audio = "oml/{0}".format(
            self.campana_dialer.queue_campana.audio_para_contestadores.get_filename_audio_asterisk())
        self.assertEqual(dict_campana['AMDPLAY'], audio)
        self.assertEqual(dict_campana['TC'], "")
        self.assertEqual(dict_campana['IDJSON'], "")
        self.assertEqual(dict_campana['PERMITOCCULT'], "")
        self.assertEqual(dict_campana['MAXCALLS'], "")
        self.assertEqual(dict_campana['FAILOVER'], "")

    def test_devuelve_correctamente_dict_agente_asterisk(self):
        """
        este test testea el diccionario de la family del agente
        """
        servicio = AgenteFamily()
        dict_agente = servicio.create_dict(self.agente)

        self.assertItemsEqual(['SIP', 'STATUS'], dict_agente.keys())

    def test_falla_dict_agente_asterisk(self):
        """
        este test testea el diccionario de la family del agente
        """
        servicio = AgenteFamily()
        dict_agente = servicio.create_dict(self.agente)

        self.assertNotIn('PASS', dict_agente.keys())

    def test_devuelve_correctamente_values_agente_asterisk(self):
        """
        este test testea los values del diccionario de la family del agente
        """
        servicio = AgenteFamily()
        dict_agente = servicio.create_dict(self.agente)

        self.assertEqual(dict_agente['SIP'], self.agente.sip_extension)
        self.assertEqual(dict_agente['STATUS'], "")

    def test_devuelve_correctamente_values_ruta(self):
        """
        este test los values del diccionario para la family de la ruta
        """
        ruta = RutaSalienteFactory()
        patron_1_1 = PatronDeDiscadoFactory(ruta_saliente=ruta)
        patron_1_2 = PatronDeDiscadoFactory(ruta_saliente=ruta)

        servicio = RutaSalienteFamily()

        # verifico que genere correctamente el dict de la ruta
        dict_ruta = servicio.create_dict_ruta(ruta)

        self.assertEqual(dict_ruta['NAME'], ruta.nombre)
        self.assertEqual(dict_ruta['RINGTIME'], ruta.ring_time)
        self.assertEqual(dict_ruta['OPTIONS'], ruta.dial_options)
        self.assertEqual(dict_ruta['TRUNKS'], len(ruta.secuencia_troncales.all()))

        # verifico que genere correctamente el dict de los patrones de desicado
        dict_patron = servicio.create_dict_patron(patron_1_1)
        self.assertEqual(dict_patron['PREFIX'], len(str(patron_1_1.prefix)))
        self.assertEqual(dict_patron['PREPEND'], patron_1_1.prepend)
        dict_patron = servicio.create_dict_patron(patron_1_1)
        self.assertEqual(dict_patron['PREFIX'], len(str(patron_1_2.prefix)))
        self.assertEqual(dict_patron['PREPEND'], patron_1_2.prepen)

    def test_devuelve_correctamente_values_troncales(self):
        """
        este test los values del diccionario para la family de los troncales
        """
        troncal_1 = TroncalSIPFactory()
        troncal_2 = TroncalSIPFactory()

        servicio = TrunkFamily()

        # verifico que genere correctamente el dict de los troncales
        dict_troncal = servicio.create_dict(troncal_1)
        self.assertEqual(dict_troncal['NAME'], troncal_1.nombre)
        self.assertEqual(dict_troncal['CHANNELS'], troncal_1.canales_maximos)
        self.assertEqual(dict_troncal['CALLERID'], troncal_1.caller_id)

        dict_troncal = servicio.create_dict(troncal_2)
        self.assertEqual(dict_troncal['NAME'], troncal_2.nombre)
        self.assertEqual(dict_troncal['CHANNELS'], troncal_2.canales_maximos)
        self.assertEqual(dict_troncal['CALLERID'], troncal_2.caller_id)
