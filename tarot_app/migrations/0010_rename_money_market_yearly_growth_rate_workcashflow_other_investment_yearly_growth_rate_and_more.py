# Generated by Django 4.0.4 on 2022-05-12 07:08

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('tarot_app', '0009_workcashflow_added_yearly_to_retirement_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workcashflow',
            old_name='money_market_yearly_growth_rate',
            new_name='other_investment_yearly_growth_rate',
        ),
        migrations.AlterField(
            model_name='changeinexpenses',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 384969, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='changeinincome',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 384278, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='goal',
            name='dollar_value_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 385791, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='onetimeinvestment',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 386558, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='recurringinvestment',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 387263, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='workcashflow',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 5, 12, 7, 8, 2, 383412, tzinfo=utc)),
        ),
    ]