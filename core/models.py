from django.db import models

# Create your models here.


class Contact(models.Model):
    user_id = models.CharField(
        max_length=20,
        db_column="user_id",
        verbose_name="User ID",
        help_text="User ID number in Telegram"
    )
    first_name = models.CharField(
        max_length=50,
        db_column="first_name",
        verbose_name="First Name",
        help_text="Contact first Name"
    )
    last_name = models.CharField(
        max_length=50,
        db_column="last_name",
        verbose_name="Last Name",
        help_text="Contact last name"
    )
    phone_number = models.CharField(
        max_length=20,
        db_column="phone_number",
        verbose_name="Phone Number",
        help_text="Contact phone number"
    )

    def __str__(self):
        return self.first_name

    class Meta:
        db_table = "contact"


class ChatHeader(models.Model):

    name = models.CharField(
        max_length=14,
        db_column='name',
        verbose_name='Name',
        help_text='Command name'
    )

    description = models.TextField(
        db_column='description',
        verbose_name='Description',
        help_text='Command description'
    )

    configuration = models.TextField(
        db_column='configuration',
        verbose_name='Configuration',
        help_text='Command configuration'
    )

    report_db = models.TextField(
        db_column='report_db',
        verbose_name='Report DB',
        help_text='Header report_db',
        null=True
    )

    company = models.CharField(
        max_length=50,
        db_column='company',
        verbose_name='Company',
        help_text='Header company',
        null=True
    )

    user_id = models.ForeignKey(Contact, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_header'


class ChatBody(models.Model):

    name = models.CharField(
        max_length=14,
        db_column='name',
        verbose_name='Name',
        help_text='Body name'
    )

    description = models.TextField(
        db_column='description',
        verbose_name='Description',
        help_text='Body description'
    )

    sql = models.TextField(
        db_column='sql',
        verbose_name='SQL',
        help_text='Query to be executed'
    )

    type = models.CharField(
        max_length=20,
        db_column='type',
        verbose_name='Type',
        help_text='Type of graph'
    )

    configuration = models.TextField(
        db_column='configuration',
        verbose_name='Configuration',
        help_text='Body configuration'
    )

    header_id = models.ForeignKey(ChatHeader, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_body'
