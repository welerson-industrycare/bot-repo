import json

from django.db import connections


class DynamicPivot:

    @staticmethod
    def EntityConfig(kwargs=None):
        map = dict()

        dbclient = kwargs['db_key'] if kwargs is not None else 'default'
        cur = connections[dbclient].cursor()
        try:
            data = []
            cur.execute('SELECT key, value FROM system_config ', [])

            desc = cur.description 
            data = [ dict(zip([col[0] for col in desc], row)) for row in cur.fetchall() ]
            map.update({ 'generalConfig': json.loads( [ d for d in data if d['key'] == 'generalConfig' ][0]['value'] ) })
            map.update({ 'metricQuery': json.loads( [ d for d in data if d['key'] == 'metricQuery' ][0]['value'] ) })
            map.update({ 'dimensionQuery': json.loads( [ d for d in data if d['key'] == 'dimensionQuery' ][0]['value'] ) })
            map.update({ 'filterQuery': json.loads( [ d for d in data if d['key'] == 'filterQuery' ][0]['value'] ) })
            map.update({ 'joinQuery': json.loads( [ d for d in data if d['key'] == 'joinQuery' ][0]['value'] ) })

            cur.close()
        except Exception as e:
            cur.close()
            raise e

        return map

    @staticmethod
    def UtilityMetrics(parameters):
        utilities = {}
        #dbclient = db_client(request)
        dbclient = parameters['db_key']
        cur = connections[dbclient].cursor()
        try:
            data = []
            cur.execute('SELECT plant_equipment_nature_id, name, un, aggregation, app_id, company_id FROM plant_equipment_nature; ', [])

            desc = cur.description 
            data = [ dict(zip([col[0] for col in desc], row)) for row in cur.fetchall() ]
            cur.close() 

            for e in [e for e in data if e['name'] not in ('ENERGIA', 'ENERGIA ELÉTRICA')]:
                if e['aggregation'] == 'avg':
                    utilities["%s_%s"%(e['name'], e['plant_equipment_nature_id'])] = dict(
                        source="utility",
                        label=e['name'],
                        query="""NULLIF(sum( CASE WHEN e.plant_equipment_nature_id = %s THEN a.value ELSE 0 END )::float, 0)"""%(e['plant_equipment_nature_id']),
                        conf=[["%s_COUNT_%s"%(e['name'], e['plant_equipment_nature_id'])], None, True, False, 0, ['ameanAgg'], 0, ['ameanAgg']],
                        Join=["EQP"]
                    )
                    utilities["%s_COUNT_%s"%(e['name'], e['plant_equipment_nature_id'])] = dict(
                        source="utility",
                        label='%s(Count)'%(e['name']),
                        query="""NULLIF(sum( CASE WHEN e.plant_equipment_nature_id = %s THEN 1 ELSE 0 END )::float, 0)"""%(e['plant_equipment_nature_id']),
                        conf=[[], None, False, False, 0, ['sum'], 0, ['sum']],
                        Join=[]
                    )
                else:
                    utilities[ "%s_%s"%(e['name'], e['plant_equipment_nature_id']) ] = dict(
                        source="utility",
                        label=e['name'],
                        query="""NULLIF(%s( CASE WHEN e.plant_equipment_nature_id = %s THEN a.value ELSE 0 END )::float, 0)"""%((e['aggregation'] if e['aggregation'] else 'sum'), e['plant_equipment_nature_id']),
                        conf=[[], None, True, False, 0, [(e['aggregation'] if e['aggregation'] else 'sum')], 0, [(e['aggregation'] if e['aggregation'] else 'sum')]],
                        Join=["EQP"]
                    )   
            
        except Exception as e:
            print(e)
            raise e
        return utilities

    @staticmethod
    def QueryBuilder(request, Config, kwargs):
        entity = DynamicPivot.EntityConfig(kwargs)
        LabelDimension = []
        LabelMetrics = []
        Joins = []
        Filters = []
        GroupBy = []
        DimensionPlainCols = []
        DimensionCols = []
        MetricCols = []
        Sources = []
        Parameters = dict()
        Result = dict(
            LabelDimension=LabelDimension,
            LabelMetrics=LabelMetrics,
            Dimensions=DimensionCols,
            DimensionsPlain=DimensionPlainCols,
            Metrics=MetricCols,
            Sources=Sources,
            Joins=Joins,
            Filters=Filters,
            Parameters=Parameters,
            Groups=GroupBy
        )

        dateColumn = entity['generalConfig']['dateColumn'] if 'dateColumn' in entity['generalConfig'] else 'datetime_read'
        if Config.date_start and Config.date_end:
            Filters.append("a." + dateColumn + " between %(DATE_FROM)s and %(DATE_TO)s")
            Parameters['DATE_FROM'] = Config.date_start
            Parameters['DATE_TO'] = Config.date_end

        # Filtros - Join de filtros são independentes de sources, filtros exclusivos de sources são ocultados da tela
        for t in Config.Filters:
            if len(t['values']) != 0:
                params = [["%s%s" % (t['key'], i), t['values'][i]]
                          for i in range(0, len(t['values']))]
                formated = ['%s(%s)s' % ('%', p[0]) for p in params]
                Filters.append(
                    entity['filterQuery'][t['key']]['query'] % (",".join(formated)))
                Parameters.update([(p[0], p[1]) for p in params])
                Joins.extend(entity['filterQuery'][t['key']]['Join'])

        # Dimensões - Join de dimensões são independentes de sources, dimensões exclusivos de sources são ocultados da tela
        for d in Config.Dimensions:
            DimensionPlainCols.append(entity['dimensionQuery'][d]['query'])
            DimensionCols.append('''%s "%s"'''%(entity['dimensionQuery'][d]['query'], entity['dimensionQuery'][d]['label']))
            LabelDimension.append(entity['dimensionQuery'][d]['label'])
            Joins.extend(entity['dimensionQuery'][d]['Join'])

        # Métricas - Segrega Joins de acordo com o source do dado
        total_metrics = {**entity['metricQuery'], **DynamicPivot.UtilityMetrics(kwargs)}
        source_map = list(set( [ total_metrics[d]['source'] for d in Config.Metrics] ))
        [ Result.update({ 'Joins_' + s: Joins[:] }) for s in source_map]
        for d in Config.Metrics:
            MetricCols.append('''%s "%s"'''%(total_metrics[d]['query'], total_metrics[d]['label']))
            LabelMetrics.append(total_metrics[d]['label'])
            c_source = total_metrics[d]['source']
            Sources.append(c_source)
            Result['Joins_' + c_source].extend(total_metrics[d]['Join'])
            if 'excludeDimension' in total_metrics[d]:
                Result['Joins_' + c_source] =  [ r for r in Result['Joins_' + c_source] if r not in total_metrics[d]['excludeDimension'] ]

        GroupBy = sorted([entity['dimensionQuery'][x]
                          for x in Config.Dimensions], key=lambda d: d['OrderID'])
        GroupBy = [g['Group'] for g in GroupBy if g['Group'] != '']

        for s in source_map:
            Result['Joins_' + s] = sorted([entity['joinQuery'][x]
                        for x in list(set(Result['Joins_' + s]))], key=lambda d: d['OrderID'])
            Result['Joins_' + s] = [j['query'] for j in Result['Joins_' + s]]


        Result["Groups"] = GroupBy
        return Result
