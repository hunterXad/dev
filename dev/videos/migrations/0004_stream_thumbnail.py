# Generated by Django 5.2.3 on 2025-06-26 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_category_category_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='stream',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails-stream/'),
        ),
    ]
