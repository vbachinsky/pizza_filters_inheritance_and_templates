# Generated by Django 2.2.8 on 2019-12-16 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resetpassworddata',
            name='token',
            field=models.CharField(blank=True, default='704a9bafe11f42fcb7e7a7fd8f0ba2eca0125c85b93542c3a05319e97625ccd9', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(blank=True, default='f989fba8eecf40e4be7472e664fd017a5d4e848022fe44f78254ed536c719f57', max_length=300, null=True),
        ),
    ]