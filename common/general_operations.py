from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta

def get_datefilters():
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    from_to = dict()
    from_to['Hoje']=[ 'now()::date', '''now()::date + interval '1 day' - interval '1 minute' ''',
        now, now + timedelta(days=1) - timedelta(minutes=1)]
    from_to['Ontem']=[''' now()::date - interval '1 day' ''', '''now()::date - interval '1 minute' ''',
        now - timedelta(days=1), now - timedelta(minutes=1)] 
    from_to['Últimos 7 Dias']=[''' now()::date - interval '6 day' ''', '''now()::date + interval '1 day' - interval '1 minute' ''',
        now - timedelta(days=6), now + timedelta(days=1) - timedelta(minutes=1)] 
    from_to['Últimos 30 Dias']=[''' now()::date - interval '29 day' ''', '''now()::date + interval '1 day' - interval '1 minute' ''',
        now - timedelta(days=29), now + timedelta(days=1) - timedelta(minutes=1)]
    from_to['Mês Anterior']=['''to_char(now(), 'YYYY-MM-01')::date - interval '1 month' ''', ''' to_char(now(), 'YYYY-MM-01')::date - interval '1 minute' ''',
        now.replace(day=1) - relativedelta(months=1), now.replace(day=1) - timedelta(minutes=1)]
    from_to['Mês Atual']=[''' to_char(now(), 'YYYY-MM-01')::date ''', ''' to_char(now(), 'YYYY-MM-01')::date + interval '1 month' - interval '1 minute' ''',
        now.replace(day=1), now.replace(day=1) + relativedelta(months=1) - timedelta(minutes=1)]
    from_to['Últimos 6 Meses']=['''now()::date - interval '12 months' ''', '''now()::date + interval '1 day' - interval '1 minute' ''',
        now - relativedelta(months=6), now + timedelta(days=1) - timedelta(minutes=1)]
    from_to['Ano Passado']=['''to_char(now(), 'YYYY-01-01')::date - interval '1 year' ''', '''to_char(now(), 'YYYY-01-01')::date  - interval '1 minute' ''',
        now.replace(month=1 ,day=1) - relativedelta(years=1), now.replace(month=1 ,day=1) - timedelta(minutes=1)]
    from_to['Ano Atual']=['''to_char(now(), 'YYYY-01-01')::date ''', '''to_char(now(), 'YYYY-01-01')::date + interval '1 year' - interval '1 minute' ''',
        now.replace(month=1 ,day=1), now.replace(month=1 ,day=1) + relativedelta(years=1) - timedelta(minutes=1)]
    from_to['Últimos 12 Meses']=['''now()::date - interval '12 months' ''', '''now()::date + interval '1 day' - interval '1 minute' ''',
        now - relativedelta(months=12), now + timedelta(days=1) - timedelta(minutes=1)]

    return from_to