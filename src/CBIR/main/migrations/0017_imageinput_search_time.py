# Generated by Django 4.2.7 on 2023-11-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_alter_imagedataset_similarity'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageinput',
            name='search_time',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=9),
        ),
    ]
