# Generated by Django 4.2.7 on 2023-11-15 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_imagedataset_similarity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedataset',
            name='similarity',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=13, null=True),
        ),
    ]
