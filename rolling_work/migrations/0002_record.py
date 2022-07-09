# Generated by Django 3.2.5 on 2022-07-08 11:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rolling_work', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_stamp', models.DateTimeField(auto_now_add=True)),
                ('longest_work_period', models.IntegerField(default=0)),
                ('shortest_work_period', models.IntegerField(default=0)),
                ('longest_rest_period', models.IntegerField(default=0)),
                ('shortest_rest_period', models.IntegerField(default=0)),
                ('work_total', models.IntegerField(default=0)),
                ('app_total', models.IntegerField(default=0)),
                ('roll_count', models.IntegerField(default=0)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
