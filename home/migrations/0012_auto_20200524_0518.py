# Generated by Django 3.0.4 on 2020-05-24 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20200518_0536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(choices=[('Closed', 'Closed'), ('False', 'Read'), ('True', 'New')], default='new', max_length=10),
        ),
    ]
