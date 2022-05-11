# Generated by Django 4.0.4 on 2022-05-11 05:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tarot_app', '0002_remove_workcashflow_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='goal',
            old_name='goal_date',
            new_name='dollar_value_date',
        ),
        migrations.AlterField(
            model_name='changeinexpenses',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 5, 34, 12, 822837, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changeinincome',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 5, 34, 12, 822275, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='onetimeinvestment',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 5, 34, 12, 824021, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='recurringinvestment',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 5, 34, 12, 824581, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='workcashflow',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 11, 5, 34, 12, 821730, tzinfo=utc)),
        ),
    ]