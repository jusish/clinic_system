# Generated by Django 5.1.2 on 2024-10-23 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dob', models.DateField()),
                ('contact_info', models.CharField(max_length=100)),
                ('date_attended', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
