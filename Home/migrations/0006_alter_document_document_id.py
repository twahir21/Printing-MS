# Generated by Django 4.0.7 on 2023-10-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_alter_document_document_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document_id',
            field=models.AutoField(primary_key=True, serialize=False, unique=True),
        ),
    ]
