# Generated by Django 5.1.4 on 2025-01-25 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers_rename_user_payment_owner_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
