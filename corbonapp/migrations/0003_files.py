# Generated by Django 3.0.8 on 2020-07-07 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('corbonapp', '0002_privatedocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(null=True, upload_to='excel_file/')),
            ],
        ),
    ]
