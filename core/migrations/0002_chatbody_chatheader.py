# Generated by Django 3.1.6 on 2021-02-18 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Header name', max_length=14, verbose_name='Name')),
                ('description', models.TextField(db_column='description', help_text='Header description', verbose_name='Description')),
                ('configuration', models.TextField(db_column='configuration', help_text='Header configuration', verbose_name='Configuration')),
                ('report_db', models.TextField(db_column='report_db', help_text='Header report_db', verbose_name='Report DB')),
                ('company', models.CharField(db_column='company', help_text='Header company', max_length=50, verbose_name='Company')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.contact')),
            ],
            options={
                'db_table': 'chat_header',
            },
        ),
        migrations.CreateModel(
            name='ChatBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_column='name', help_text='Body name', max_length=14, verbose_name='Name')),
                ('description', models.TextField(db_column='description', help_text='Body description', verbose_name='Description')),
                ('sql', models.TextField(db_column='sql', help_text='Query to be executed', verbose_name='SQL')),
                ('type', models.CharField(db_column='type', help_text='Type of graph', max_length=20, verbose_name='Type')),
                ('configuration', models.TextField(db_column='configuration', help_text='Body configuration', verbose_name='Configuration')),
                ('header_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.chatheader')),
            ],
            options={
                'db_table': 'chat_body',
            },
        ),
    ]