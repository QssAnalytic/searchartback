# Generated by Django 4.2.2 on 2023-12-07 06:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
            ],
            options={
                'verbose_name': 'Sector',
                'verbose_name_plural': 'Sectors',
            },
        ),
        migrations.CreateModel(
            name='SubSect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subsector', models.CharField(blank=True, max_length=100, null=True)),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sect')),
            ],
            options={
                'verbose_name': 'Subsector',
                'verbose_name_plural': 'Subsectors',
            },
        ),
        migrations.CreateModel(
            name='Indica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('indicator', models.CharField(max_length=250)),
                ('content', models.TextField(blank=True, null=True)),
                ('subsector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.subsect')),
            ],
            options={
                'verbose_name': 'Indicator',
                'verbose_name_plural': 'Indicators',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('country_code2', models.CharField(blank=True, max_length=100, null=True)),
                ('country_code', models.CharField(blank=True, max_length=100, null=True)),
                ('rank', models.BigIntegerField(blank=True, null=True)),
                ('amount', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('indicator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.indica')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
    ]