import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy as np


def build_bar_column_chart(chart, queryset, properties, title, style='ggplot'):
    """
    Creates bar, stackedbar, column and stacked column chart
    :param db: str database name
    :param sql: str with query for execute on database
    :return pyplot object
    """

    # set graph style
    plt.style.use(style)

    # extract data from result and convert tuples into list
    data = [list(row) for row in queryset.get("queryset","") ]

    objects = tuple([column[0] for column in data])
    values = [column[1] for column in data] 
    aux = np.arange(len(objects))

    if chart == 'bar':

        # creates bar chart
        plt.barh(aux, values, align=properties.get('align', 'center'), alpha=properties.get('alpha', 0.7))
        plt.yticks(aux, objects, rotation=properties.get('rotation',45), fontsize=properties.get('fontsize',5))
        plt.xlabel(properties.get('labels',''))

    elif chart == 'column': 

        # creates column chart 
        plt.bar(aux, values, align=properties.get('align', 'center'), alpha=properties.get('alpha', 0.7))
        plt.xticks(aux, objects, rotation=properties.get('rotation',45), fontsize=properties.get('fontsize',5))
        plt.ylabel(properties.get('labels',''))

    return plt


def build_table(type, queryset, properties, title,  style='ggplot'):
    """
    Creates table
    :param db: str database name
    :param sql: str with query for execute on database
    :return pyplot object
    """

    # set graph style
    plt.style.use(style)

    # extract data from result and convert tuples into list
    data = [list(row) for row in queryset.get("queryset","") ]

    # get heads for table
    names = queryset.get("names","")

    plt.axis('off')

    # creates table 
    table = plt.table(
        cellText=data,
        colLabels=names, 
        loc=properties.get("loc")
    )

    for (row, col), cell in table.get_celld().items():
        if (row == 0):
            cell.set_text_props(fontproperties=FontProperties(weight='bold'))

    return plt


def build_scatter_chart(queryset, properties, style='ggplot'):
    """
    Creates scatter chart
    :param db: str database name
    :param sql: str with query for execute on database
    :return pyplot object
    """

    # set graph style
    plt.style.use(style)

    # extract data from result and convert tuples into list
    data = [list(row) for row in queryset.get("queryset","") ]

    x = [column[0] for column in data]
    y = [column[1] for column in data]

    plt.scatter(x,y)
    
    return plt


def build_line_chart(queryset, properties, style='ggplot'):
    """
    Creates line chart
    :param db: str database name
    :param sql: str with query for execute on database
    :return pyplot object
    """

    # set graph style
    plt.style.use(style)

    # extract data from result and convert tuples into list
    data = [list(row) for row in queryset.get("queryset","") ]

    x = [column[0] for column in data]
    y = [column[1] for column in data]

    plt.plot(x,y)

    return plt


def build_pie_chart(type, queryset, properties, title,style='ggplot'):
    """
    Creates pie chart
    :param db: str database name
    :param sql: str with query for execute on database
    :return pyplot object
    """

    # set graph style
    plt.style.use(style)

    # extract data from result and convert tuples into list
    data = [list(row) for row in queryset.get("queryset","") ]

    labels = [column[0] for column in data] 
    values = [column[1] for column in data] 

    plt.pie(values, labels=labels, autopct='%1.1f%%', shadow=True)

    return plt

