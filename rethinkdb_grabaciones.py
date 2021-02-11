import os

from rethinkdb import r

OML_RETHINKDB_HOST = 'oml-rethinkdb_1-devenv'
OML_RETHINKDB_PORT = 28015

RUTA_GRABABACIONES = '/var/spool/asterisk/monitor/'
# RUTA_GRABABACIONES = '/opt/omnileads/asterisk/var/spool/asterisk/monitor' en AIO

connection = r.connect(OML_RETHINKDB_HOST, OML_RETHINKDB_PORT, db='omnileads')
# connection = r.connect(settings.OML_RETHINKDB_HOST, settings.OML_RETHINKDB_PORT, db='omnileads')

r.db_create("omnileads").run(connection)

r.table_create('grabaciones').run(connection)


def save_file(file_path, save_name):
    """
    Store the file at 'file_path' with the filename 'save_name'.
    """
    fh = open(file_path, 'rb')
    contents = fh.read()
    fh.close()
    r.table('grabaciones').insert({
        'filename': save_name,
        'file': r.binary(contents)
    }).run(connection)


for root, dirs, files in os.walk(RUTA_GRABABACIONES):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))
    for rec_file in files:
        path_rec_file = os.path.join(root, rec_file)
        save_file(path_rec_file, rec_file)
