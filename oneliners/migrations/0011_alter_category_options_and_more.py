# Generated by Django 4.2.5 on 2023-09-28 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oneliners', '0010_alter_category_unique_together'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterModelOptions(
            name='onelinercategory',
            options={'verbose_name_plural': 'oneliner categories'},
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
