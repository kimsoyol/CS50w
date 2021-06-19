# Generated by Django 3.2.4 on 2021-06-19 05:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='categories',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='itemCategory', to='auctions.category'),
        ),
    ]