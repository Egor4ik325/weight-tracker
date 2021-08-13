# Generated by Django 3.2.4 on 2021-06-22 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_alter_recipe_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='weight',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.FloatField(default=100),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='description',
            field=models.TextField(),
        ),
    ]