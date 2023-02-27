# Generated by Django 4.0 on 2022-08-27 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('name', models.CharField(max_length=50)),
                ('gender', models.CharField(max_length=6)),
                ('address', models.TextField()),
                ('pincode', models.IntegerField(max_length=6)),
                ('contactno', models.CharField(max_length=15)),
                ('emailaddress', models.EmailField(max_length=50, primary_key=True, serialize=False)),
                ('regdate', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Login',
            fields=[
                ('userid', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=20)),
                ('usertype', models.CharField(max_length=30)),
            ],
        ),
    ]
