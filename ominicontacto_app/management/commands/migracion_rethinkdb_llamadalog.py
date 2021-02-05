from django.core.management.base import BaseCommand

from reportes_app.models import LlamadaLog

from rethinkdb import r

OML_RETHINKDB_HOST = 'oml-rethinkdb_1-devenv'
OML_RETHINKDB_PORT = 28015

RUTA_GRABABACIONES = '/var/spool/asterisk/monitor/'
# RUTA_GRABABACIONES = '/opt/omnileads/asterisk/var/spool/asterisk/monitor' en AIO


class Command(BaseCommand):

    def handle(self, *args, **options):
        connection = r.connect(OML_RETHINKDB_HOST, OML_RETHINKDB_PORT, db='omnileads')

        r.table_create('llamada_log').run(connection)

        for llamada_log in LlamadaLog.objects.all():
            llamada_log_dict = llamada_log.__dict__
            del llamada_log_dict['_state']
            r.table('llamada_log').insert(llamada_log_dict).run(connection)

        print('LlamadaLog was upload to RethinkDB!')
