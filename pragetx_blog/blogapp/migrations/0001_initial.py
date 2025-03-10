# Generated by Django 5.0.7 on 2024-07-12 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='trackingData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campaign', models.CharField(blank=True, max_length=255, null=True, verbose_name='Campaign')),
                ('medium', models.CharField(blank=True, max_length=255, null=True, verbose_name='Medium')),
                ('page', models.CharField(blank=True, max_length=255, null=True, verbose_name='Page')),
                ('ref', models.CharField(blank=True, max_length=255, null=True, verbose_name='Ref')),
                ('source', models.CharField(blank=True, max_length=255, null=True, verbose_name='Source')),
            ],
        ),
    ]
