# Generated by Django 4.2.1 on 2023-05-28 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cajero', '0005_alter_factura_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='fecha',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]