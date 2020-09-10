# Generated by Django 3.0.8 on 2020-09-09 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_dog'),
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='account',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments_wrote', to='account.Account'),
        ),
    ]
