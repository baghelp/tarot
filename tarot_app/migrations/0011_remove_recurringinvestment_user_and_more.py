# Generated by Django 4.1 on 2022-08-28 07:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tarot_app', '0010_rename_money_market_yearly_growth_rate_workcashflow_other_investment_yearly_growth_rate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringinvestment',
            name='user',
        ),
        migrations.AlterField(
            model_name='changeinexpenses',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 28, 7, 25, 16, 216663, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='changeinincome',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 28, 7, 25, 16, 216177, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='goal',
            name='dollar_value_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 28, 7, 25, 16, 217135, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='workcashflow',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 28, 7, 25, 16, 215508, tzinfo=datetime.timezone.utc)),
        ),
        migrations.DeleteModel(
            name='OneTimeInvestment',
        ),
        migrations.DeleteModel(
            name='RecurringInvestment',
        ),
    ]
