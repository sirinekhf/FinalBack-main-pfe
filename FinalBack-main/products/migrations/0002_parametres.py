# Generated by Django 3.1 on 2023-06-26 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametres',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('tva', models.FloatField(null=True)),
                ('logo', models.BinaryField(null=True)),
                ('company_name', models.CharField(max_length=255)),
            ],
        ),
    ]
