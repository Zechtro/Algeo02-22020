# Generated by Django 4.2.7 on 2023-11-15 02:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_imagedataset_similiarity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imagedataset',
            old_name='similiarity',
            new_name='similarity',
        ),
    ]
