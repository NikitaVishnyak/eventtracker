# Generated by Django 4.2 on 2023-06-10 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cities_light', '0011_alter_city_country_alter_city_region_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventCategories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name_plural': 'EventCategories',
            },
        ),
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_confirmed', models.BooleanField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caterories', to='eventsapp.eventcategories')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.city')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cities_light.country')),
            ],
            options={
                'verbose_name_plural': 'Events',
            },
        ),
    ]