# Generated by Django 3.0.4 on 2020-05-16 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_auto_20200516_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactformmessage',
            name='status',
            field=models.CharField(choices=[('True', 'New'), ('False', 'Read'), ('Closed', 'Closed')], default='new', max_length=10),
        ),
    ]
