# Generated by Django 4.0.10 on 2023-09-22 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_confirmationcode_user_confirmationcode_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmationcode',
            name='email',
            field=models.EmailField(default='noemail@example.com', max_length=254),
        ),
    ]
