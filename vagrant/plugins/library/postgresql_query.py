#!/usr/bin/python
# Copyright (c) 2016 Patrick Schoenfeld
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
DOCUMENTATION = '''
---
module: postgresql_query
short_description: Run arbitrary SQL query against a PostgreSQL database
description:
   - Run arbitrary SQL query against a PostgreSQL database
   - This modules allows you to run arbitrary SQL queries against a
     PostgreSQL database.
   - For idempotency it's possible to specify an SQL query as unless statement,
     which is run with SELECT EXISTS.
options:
  database:
    description:
      - name of database against which the psql command will be run
      - 'Alias: I(db)'
    required: yes
  query:
    description:
      - specify a query to be executed
    required: yes
  unless:
    description:
      - specify an SQL query to run against the database in order to check
        if the psql commands needs to be run at all.
  port:
    description:
      - Database port to connect to.
    required: no
    default: 5432
  login:
    description:
      - User used to authenticate with PostgreSQL
      - 'Alias: I(login_user)'
    required: no
    default: postgres
  host:
    description:
      - Host running PostgreSQL where you want to execute the actions.
      - 'Alias: I(login_host)'
    required: no
    default: localhost
notes:
   - The default authentication assumes that you are either logging in as or
     sudo'ing to the postgres account on the host.
   - This module uses psycopg2, a Python PostgreSQL database adapter. You must
     ensure that psycopg2 is installed on the host before using this module. If
     the remote host is the PostgreSQL server (which is the default case), then
     PostgreSQL must also be installed on the remote host. For Ubuntu-based
     systems, install the postgresql, libpq-dev, and python-psycopg2 packages
     on the remote host before using this module.
requirements: [ psycopg2 ]
author: "Patrick Schoenfeld (@aptituz)"
'''

EXAMPLES = '''
#  Alter a role unless the role's field already has the required value
- postgresql_query db=test command='ALTER ROLE foo SET statement_timeout = 1' unless="SELECT 1 FROM pg_roles WHERE rolname = 'foo' AND rolconfig @> ARRAY['statement_timeout=1']"
'''

import itertools
import os.path
import string

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

def need_to_run(cursor, unless_query):
    """Runs given unless query against database to check if psql needs to run"""
    query = 'SELECT EXISTS (' + unless_query + ') foo'
    cursor.execute(query)
    return cursor.fetchone()[0] == False

def execute_query(cursor, query):
  """Execute given query"""
  cursor.execute(query)
  return cursor.rowcount

def main():
    module = AnsibleModule(
        argument_spec           = dict(
            query               = dict(type='str', required=True),
            unless              = dict(type='str'),
            database            = dict(required=True, aliases=['db']),
            host                = dict(aliases=['login_host']),
            password            = dict(default='',type='str', aliases=['login_password']),
            port                = dict(type='int', default=5432),
            login               = dict(default='postgres', aliases=['login_user']),
        ),
        supports_check_mode = True
    )

    if not HAS_PSYCOPG2:
        module.fail_json(msg="the python psycopg2 module is required")

    params_map = {
                      "host": "host",
                     "login": "user",
                  "password": "password",
                      "port": "port",
                  "database": "database"
    }
    kw = dict( (params_map[k], v) for (k, v) in module.params.iteritems()
              if k in params_map and v != "" )

    try:
        db_connection = psycopg2.connect(**kw)
        cursor = db_connection.cursor()
    except Exception, e:
        module.fail_json(msg="unable to connect to database: %s" % e)

    if module.params['unless'] != None:
      if not need_to_run(cursor, module.params['unless']):
        kw['changed']  = False
        kw['msg']      = "skipping query execution, due to unless statement"
        kw['rowcount'] = 0
    else:
      cursor.execute(module.params['query'])
      kw['rowcount'] = cursor.rowcount
      kw['changed']  = True

      if module.check_mode:
        db_connection.rollback()
      else:
        db_connection.commit()

    module.exit_json(**kw)

from ansible.module_utils.basic import AnsibleModule

if __name__ == '__main__':
    main()
