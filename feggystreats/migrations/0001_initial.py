# Generated by Django 3.1.1 on 2021-11-19 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=500)),
                ('category', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='uploads/')),
            ],
        ),
    ]
