import re

from datetime import datetime

from django.db import connections
from django.db import models

def sql_services_integrate(integrators, sql):
    ctes = []

    pattern = re.compile( str.join('|', [ r'\b' + i.nome_msi + r'\b' for i in integrators] ) )
    for c in list(set(re.findall(pattern, sql))):
        curr = [ i for i in integrators if i.nome_msi == c][0]
        ctes.append( f' {curr.nome_msi}( {curr.flab_msi} ) as ( \n\n{curr.sql_msi}\n\n )' )

    if len(ctes) > 0:
        ctes.append( f' original_sql_cte as ( \n{sql}\n ) ' )
        ctes = str.join( ',\n', ctes )
        return f"""with { ctes } 
            select * from original_sql_cte
        """
    else:
        return sql

def virtual_orm(source='default'):
    entities = dict()
    timezone = 'America/Sao_Paulo'
    cur = connections[source].cursor()
    try:
        prefix = '' if source == 'default' else source + '_'
        query = 'SELECT nome_msi, flab_msi, sql_msi FROM public.multiserviceintegrator'

        cur.execute( query )
        services = cur.fetchall()
        for row in services:
            if row[2] != '':
                cur.execute( f'with curr_cte({row[1]}) as (\n\n\t{row[2]}\n\n) select * from curr_cte' )
                desc = cur.description 
                entities[row[0]] = [ dict(zip([col[0] for col in desc], row)) for row in cur.fetchall() ]
            else:
                entities[row[0]] = []
        cur.close()
    except Exception as e:
        print('\n\n-------------------------------------------------\n\n' +
            'Ocorreu um erro ao buscar uma entidade virtualizada: \n\n' + 
            '\n\n\nCódigo do erro: ' +
            str(e) +
            '\n\n-------------------------------------------------\n\n'
        )
        return entities

    return entities

def current_service_integrator(db_model, source='default'):
    def db_evaluate(f, obj):
        field = getattr(obj, f.name)
        if field is None:
            return 'null'
        elif isinstance(field, int) or isinstance(field, float):
            return str(field)
        elif isinstance(field, str):
            return '\'' + field.replace("\'", "\'\'").replace('%', 'escapePercent') + '\''
        elif isinstance(field, datetime):
            return '\'' + field.strftime("%Y-%m-%d %H:%M:%S") + '\'::timestamp with time zone'
        elif isinstance(field, models.fields.files.ImageFieldFile):
            return '\'' + str(field) + '\''
        elif type(f).__name__ in ['ForeignKey', 'OneToOneField']:
            field_internal = field.pk
            return str(field_internal)
        else:
            return field

    def default_values(f):
        f = f.foreign_related_fields[0] if type(f).__name__ in ['ForeignKey', 'OneToOneField'] else f
        if f.description == 'Integer':
            return '-1'
        elif 'String' in f.description:
            return "''"
        elif 'Boolean' in f.description:
            return 'false'
        elif 'Date (without time)' in f.description:
            return 'now()::date'
        elif 'Email address' in f.description:
            return "''"
        elif 'File' in f.description:
            return "''"
        else:
            return 'null'

    entities = []
    prefix = '' if source == 'default' else source + '_'
    for e in db_model:  # classes
        sql_cte = ['(' + str.join(', ', [ db_evaluate(f, obj) for f in e._meta.fields ]) + ')' for obj in e.objects.using(source).all() ]
        entities.append({
            'nome_msi': prefix + e._meta.db_table,
            'flab_msi': str.join(', ', [f.name for f in e._meta.fields]),
            'sql_msi': 'values ' + str.join(',\n', sql_cte) if str.join(',\n', sql_cte) != '' else 'select ' + str.join(', ', [default_values(f) for f in e._meta.fields]) + ' limit 0'
        })

    return entities
