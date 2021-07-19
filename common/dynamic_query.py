import datetime

from django.conf import settings
from django.db import connections
from common.dynamic_pivot import DynamicPivot
from common.general_classes import ConfigQuery

INTERVAL_TEMPLATES = {"hours": 'HH24:00',
                      "week": 'DD/MM', "month": 'MM/YYYY', "year": 'YYYY'}


def GetPivotData(content, request, kwargs):
    Config = content
    if Config.date_start and Config.date_end and Config.date_start > Config.date_end:
        raise Exception(
            "Ocorreu um erro: O período informado possui uma data de início posterior a data de término")

    timezone = 'UTC'
    columnName = []
    result_query = []
    dbclient = kwargs['db_key']
    cur = connections[dbclient].cursor()
    try:
        result = """
            select %(dimensions)s, %(metrics)s FROM base a
            %(joins_source)s
            where %(filters)s
            group by %(groups)s
        """

        builder = DynamicPivot.QueryBuilder(request, Config, kwargs)
        sources = list(set(builder['Sources']))
        parameters = builder["Parameters"]
        f_params = dict(
            dimensions=",\n".join(builder["Dimensions"]),
            metrics=",\n".join(builder["Metrics"]),
            filters="\n and".join(builder["Filters"]),
            groups=",\n".join(builder["Groups"])
        )
        [ f_params.update({ 'metrics_' + s: ",\n".join([builder["Metrics"][b[0]] for b in enumerate(builder['Sources']) if b[1] == s]) }) for s in sources ]
        [ f_params.update({ 'joins_' + s:  "\n".join(builder["Joins_" + s])   }) for s in sources ]

        if len(sources) > 1:
            params = dict(
                dim=", ".join(['"' + b + '"' for b in builder["LabelDimension"]]),
                dimK=", ".join(['k."' + b + '"' for b in builder["LabelDimension"]]),
                mtc=", ".join(['"' + b + '"' for b in builder["LabelMetrics"]])
            )

            s_ctes, s_joins, s_keys = [], [], []
            for i in range(1, len(sources) + 1):
                s_ctes.append(f'cte{i} as (%(c{i})s)')
                s_keys.append(f'select %(dim)s from cte{i}')
                s_joins.append(f'left join cte{i} on (%(dimK_{i})s)')
                cte = result.replace('joins_source', 'joins_' + sources[i-1]).replace('metrics', 'metrics_' + sources[i-1]).replace('base', sources[i-1])
                params.update({f'c{i}': cte })
                params.update({f'dimK_{i}': " and ".join([f'k."%s" = cte{i}."%s" '%(b, b) for b in builder["LabelDimension"]]) })
        
            result_temp = f''' with { str.join(', ', s_ctes) },
                keys as (newLine select distinct %(dimK)s from (newLine  { str.join(' union ', s_keys) }   newLine) k newLine)
                select %(dimK)s, %(mtc)s from keys k
                { str.join(' newLine ', s_joins) }
            '''.replace('newLine', '\n')
            result = result_temp%(params)
        else:
            result = result.replace('joins_source', 'joins_' + sources[0]).replace('base', sources[0])
        result = result % (f_params)
        
        result = '''SET TIMEZONE = '{0}'; {1}'''.format(timezone, result)

        cur.execute(result, parameters)
        columnName = [c.name for c in cur.description]
        result_query = [row for row in cur.fetchall()]

        cur.close()
    except Exception as e:
        connections[dbclient]._rollback()
        raise e

    return {'names': columnName, 'data': result_query}

def GetPivotQuery(content, request, kwargs):
    result = """
            select %(dimensions)s, %(metrics)s FROM base a
            %(joins_source)s
            where %(filters)s
            group by %(groups)s
            order by 1
    """
    try:
        if 'fromTo' in content:
            start_date = content['fromTo'][0]
            end_date = content['fromTo'][1]
        else:
            start_date = None
            end_date = None

        Config = ConfigQuery(start_date, end_date, [e['id'] for e in content['xAxis'] ], [e['id'] for e in content['yAxis']], content['filters'])
        builder = DynamicPivot.QueryBuilder(request, Config, kwargs)
        sources = list(set(builder['Sources']))
        parameters = builder["Parameters"]
        
        f_params = dict(
            dimensions=",\n".join(builder["Dimensions"]),
            dimensions_out=( ",\n".join(builder["Dimensions"]) if content['type'] == 'table' else ('%s::text')%("::text||'-'||".join(builder["DimensionsPlain"]) ) ),
            metrics=",\n".join(builder["Metrics"]),
            filters="\n and".join(builder["Filters"]) if 'containFilters' in content else "{0}",
            groups= ",\n".join(builder["Groups"]),
            groups_out= ( ",\n".join(builder["Groups"]) if content['type'] == 'table' else '1' )
        )
        [ f_params.update({ 'metrics_' + s: ",\n".join([builder["Metrics"][b[0]] for b in enumerate(builder['Sources']) if b[1] == s]) }) for s in sources ]
        [ f_params.update({ 'joins_' + s:  "\n".join(builder["Joins_" + s])   }) for s in sources ]

        if len(sources) > 1:
            params = dict(
                dim=", ".join(['"' + b + '"' for b in builder["LabelDimension"]]),
                dimK=", ".join(['k."' + b + '"' for b in builder["LabelDimension"]]),
                dimK_out=", ".join(['k."' + b + '"' for b in builder["LabelDimension"]]) if content['type'] == 'table' else "||'-'||".join(['k."' + b + '"::text ' for b in builder["LabelDimension"]]),
                mtc=", ".join(['"' + b + '"' for b in builder["LabelMetrics"]])
            )

            s_ctes, s_joins, s_keys = [], [], []
            for i in range(1, len(sources) + 1):
                s_ctes.append(f'cte{i} as (%(c{i})s)')
                s_keys.append(f'select %(dim)s from cte{i}')
                s_joins.append(f'left join cte{i} on (%(dimK_{i})s)')
                cte = result.replace('joins_source', 'joins_' + sources[i-1]).replace('metrics', 'metrics_' + sources[i-1]).replace('base', sources[i-1])
                params.update({f'c{i}': cte })
                params.update({f'dimK_{i}': " and ".join([f'k."%s" = cte{i}."%s" '%(b, b) for b in builder["LabelDimension"]]) })
        
            result_temp = f''' with { str.join(', ', s_ctes) },
                keys as (newLine select distinct %(dimK)s from (newLine  { str.join(' union ', s_keys) }   newLine) k newLine)
                select %(dimK_out)s, %(mtc)s from keys k
                { str.join(' newLine ', s_joins) }
            '''.replace('newLine', '\n')
            result = result_temp%(params)
        else:
            result = result.replace('joins_source', 'joins_' + sources[0]).replace('dimensions', 'dimensions_out').replace('groups','groups_out').replace('base', sources[0])
        result = result % (f_params)
        
        if 'containFilters' in content:
            if 'fromTo' in content:
                result = result.replace('%(DATE_FROM)s', start_date).replace('%(DATE_TO)s', end_date)
            for fc in content['filters']:
                for i in range( 0, len(fc['values']) ):
                    result = result.replace( ('%%(%s%s)s')%( fc['key'], str(i) ), str(fc['values'][i]))

    except Exception as e:
        raise e

    return result
