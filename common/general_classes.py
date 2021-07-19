import json

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db import connections


class ConfigQuery:
    def __init__(self, date_start, date_end, dimensions, metrics, filters):
        self.date_start = date_start
        self.date_end = date_end
        self.Dimensions = dimensions
        self.Metrics = metrics
        self.Filters = filters

class AutoCompleteItem:
    def __init__(self, icon, label, key, value, table, key_type="int", url_modal="", description="", join="", index="", depends=None, cubo=True):
        self.key = key
        self.value = value
        self.table = table
        self.key_type = key_type
        self.index = index
        self.join = join
        self.icon = icon
        self.label = label
        self.url_modal = url_modal
        self.description = description
        self.depends = depends
        self.cubo = cubo

class AutoCompleteMap(object):
    
    @staticmethod
    def autocompletemap(key=None, kwargs=None):
        map = dict()

        dbclient = kwargs['db_key'] if kwargs is not None else 'default'
        cur = connections[dbclient].cursor()
        try:
            data = []
            cur.execute('SELECT key, value FROM system_config ', [])

            desc = cur.description 
            data = [ dict(zip([col[0] for col in desc], row)) for row in cur.fetchall() ]
            ac_map = json.loads( [ d for d in data if d['key'] == 'autocompletemap' ][0]['value'] )
            dependencies = json.loads( [ d for d in data if d['key'] == 'dependencies' ][0]['value'] )

            for k in ac_map.keys():
                ac_map[k]['key_type'] = ac_map[k]['key_type'] if 'key_type' in ac_map[k] else 'int'
                ac_map[k]['cubo'] = ac_map[k]['cubo'] if 'cubo' in ac_map[k] else True
                ac_map[k]['description'] = ac_map[k]['description'] if 'description' in ac_map[k] else ''
                ac_map[k]['join'] = ac_map[k]['join'] if 'join' in ac_map[k] else ''
                ac_map[k]['index'] = ac_map[k]['index'] if 'index' in ac_map[k] else ''
                ac_map[k]['url_modal'] = ac_map[k]['url_modal'] if 'url_modal' in ac_map[k] else ''
                if isinstance(ac_map[k]['depends'], dict):
                    for d in ac_map[k]['depends'].keys():
                        ac_map[k]['depends'][d]['join'] = [ dependencies[el] for el in ac_map[k]['depends'][d]['join'] ]
            map = ac_map
            cur.close()
        except Exception as e:
            cur.close()
            raise e

        if key:
            return map[key]
        else:
            return map

    @staticmethod
    def __dm(keys):
        dependencies = dict()
        #Sentido direto
        dependencies.update({'NEQ': 'left join plant_equipment_nature on plant_equipment_nature.plant_equipment_nature_id = plant_equipment.plant_equipment_nature_id'})
        dependencies.update({'PON': 'left join plant_point on plant_point.plant_point_id = plant_equipment.plant_point_id'})
        dependencies.update({'SET': 'left join plant_sector on plant_sector.plant_sector_id = plant_point.plant_sector_id'})
        dependencies.update({'UC': 'left join plant_uc on plant_uc.plant_uc_id = plant_sector.plant_uc_id'})
        
        dependencies.update({'CON': '''left join dealership on dealership.id = plant_uc.dealership_id
                                    left join person on person.id = dealership.person_id'''})
        dependencies.update({'CON2': '''left join dealership on dealership.id = plant_uc.dealership_id
                                    left join person c3 on c3.id = dealership.person_id'''})
        dependencies.update({'MCON': '''left join person_address on person_address.person_address_id=person.person_address_id
                                    left join city on city.id=person_address.city_id'''})
        dependencies.update({'MCON2': '''left join person_address on person_address.person_address_id=c3.person_address_id
                                    left join city on city.id=person_address.city_id'''})
        dependencies.update({'MCON3': '''left join person_address mc3 on mc3.person_address_id=c3.person_address_id
                                    left join city c4 on c4.city_id = mc3.city_id'''})
        dependencies.update({'UFCON': 'left join uf on uf.id=city.uf_id'})
        dependencies.update({'UFCON2': 'left join uf uf2 on uf2.uf_id=c4.uf_id'})
        dependencies.update({'UFCON3': 'left join uf on uf.id=c4.uf_id'})

        dependencies.update({'PLAN': '''left join company on company.company_id=plant_uc.company_id
                                    left join person c2 on c2.id=company.person_id'''})
        dependencies.update({'MPLAN': '''left join person_address p2 on p2.person_id = c2.id
                                    left join city mp on mp.id=p2.city_id'''})
        dependencies.update({'MPLAN2': '''left join person_address p2 on p2.person_id = person.id
                                    left join city mp on mp.id=p2.city_id'''})
        dependencies.update({'EPLAN': 'left join uf u2 on u2.id=mp.uf_id'})
        dependencies.update({'EPLAN2': 'left join uf u2 on u2.id=city.uf_id'})
        dependencies.update({'EMP': 'left join company_division on company_division.company_division_id = company.company_division_id'})
        #Sentido inverso
        dependencies.update({'IPLAN': '''left join company on company.company_division_id = company_division.company_division_id
                                    left join person c2 on c2.id=company.person_id'''})
        dependencies.update({'IUC2': 'left join plant_uc on plant_uc.company_id = company.company_id'})
        dependencies.update({'IUC': 'left join plant_uc on plant_uc.dealership_id = dealership.id'})
        dependencies.update({'ISET': 'left join plant_sector on plant_sector.plant_uc_id = plant_uc.plant_uc_id'})
        dependencies.update({'IPON': 'left join plant_point on plant_point.plant_sector_id = plant_sector.plant_sector_id'})
        dependencies.update({'IEQP': 'left join plant_equipment on plant_equipment.plant_point_id = plant_point.plant_point_id'})
        dependencies.update({'IEQP_N': 'left join plant_equipment on plant_equipment.plant_equipment_nature_id = plant_equipment_nature.plant_equipment_nature_id'})
        dependencies.update({'INEQ': 'left join plant_equipment_nature on plant_equipment_nature.plant_equipment_nature_id = plant_equipment.plant_equipment_nature_id'})

        join_list = []
        for k in keys:
            join_list.append(dependencies[k])

        return join_list
