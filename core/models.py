import requests
from django.db import models

BRAZIL_TIMEZONES = (
    ("America/Eirunepe", "America/Eirunepe"),
    ("America/Rio_Branco", "America/Rio_Branco"),
    ("America/Boa_Vista", "America/Boa_Vista"),
    ("America/Campo_Grande", "America/Campo_Grande"),
    ("America/Manaus", "America/Manaus"),
    ("America/Porto_Velho", "America/Porto_Velho"),
    ("America/Araguaina", "America/Araguaina"),
    ("America/Bahia", "America/Bahia"),
    ("America/Belem", "America/Belem"),
    ("America/Cuiaba", "America/Cuiaba"),
    ("America/Fortaleza", "America/Fortaleza"),
    ("America/Maceio", "America/Maceio"),
    ("America/Recife", "America/Recife"),
    ("America/Sao_Paulo", "America/Sao_Paulo"),
    ("America/Noronha", "America/Noronha"),
)

class MultiServiceIntegrator(models.Model):
    nome_msi = models.TextField(
        primary_key=True,
        null=False,
        db_column="nome_msi",
        verbose_name="nome_msi",
        help_text="nome_msi",
    )

    flab_msi = models.TextField(
        null=False,
        db_column="flab_msi",
        verbose_name="flab_msi",
        help_text="flab_msi",
    )

    sql_msi = models.TextField(
        null=False,
        db_column="sql_msi",
        verbose_name="sql_msi",
        help_text="sql_msi",
    )

    class Meta:
        db_table = "multiserviceintegrator"

class Contact(models.Model):
    """
    Classe que contém os dados do contato
    """
    
    user_id = models.IntegerField(
        primary_key=True,
        verbose_name="user_id",
        db_column='id',
        help_text="user_id"
        )
    contact_id = models.IntegerField(
        null=False,
        verbose_name="contact_id",
        db_column= 'contact_id',
        help_text = "contact_id",
        default=1
    )
    first_name = models.CharField(
        max_length=120,
        verbose_name="first_name",
        db_column='first_name',
        help_text="Primeiro Nome"
    )
    last_name = models.CharField(
        max_length=120,
        verbose_name="last_name",
        db_column='last_name',
        help_text="Sobrenome"
    )
    phone_number = models.CharField(
        null = False,
        verbose_name = "phone number",
        max_length=20,
        db_column = 'phone_number',
        help_text = "phone_number",
        unique=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "contact"

class BotHeader(models.Model):
    """
    Classe que representa o cabeçalho dos gráficos
    """

    botheader_id = models.AutoField(
        primary_key=True,
        verbose_name="botheader_id",
        db_column='id',
        help_text="botheader_id"
    )
    user_id = models.ForeignKey(
        Contact,
        on_delete=models.PROTECT,
        verbose_name="user_id",
        db_column='user_id',
        help_text="user_id foreignkey"
    )
    company_id = models.IntegerField(
        null = False,
        verbose_name = "Empresa",
        db_column = 'company',
        help_text = "company",
    )
    
    description = models.CharField(
        max_length=120,
        verbose_name="Descricao",
        db_column='description',
        help_text="description"
    )
    configuration = models.TextField(
        null = True,
        verbose_name="Configuração",
        db_column='configuration',
        help_text="configuration"
    )
    dbname = models.TextField(
        null = True,
        verbose_name="dbname",
        db_column='dbname',
        help_text="dbname"
    )

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "bot_header"

class BotContent(models.Model):
    """
    Classe que representa o corpo dos gráficos
    """
   
    botcontent_id = models.AutoField(
        primary_key=True,
        verbose_name="botcontent_id",
        db_column='id',
        help_text="botcontent_id"
    )
    botheader_id = models.ForeignKey(
        BotHeader,
        on_delete=models.PROTECT,
        verbose_name="botheader_id",
        db_column='botheader_id',
        help_text="botheader_id"
    )
    name = models.CharField(
        max_length=120,
        verbose_name="Nome",
        db_column='name',
        help_text="name"
    )
    description = models.CharField(
        max_length=120,
        verbose_name="Descricao",
        db_column='description',
        help_text="description"
    )
    sql = models.TextField(
        null = True,
        verbose_name="SQL",
        db_column='sql',
        help_text="Instrução SQL"
    )
    visualization_type = models.CharField(
        max_length=250,
        null = True,
        verbose_name="Tipo de Visualização",
        db_column='visualization_type',
        help_text="Tipo de visualização (Gráfico ou tabela)"
    )
    properties = models.TextField(
        null = True,
        verbose_name="Configuração ou Propriedades",
        db_column='properties',
        help_text="configuration"
    )


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "bot_content"
