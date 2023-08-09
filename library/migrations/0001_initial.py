# Generated by Django 4.2.1 on 2023-08-08 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('genre', models.CharField(max_length=33)),
                ('copy_number', models.IntegerField()),
                ('publisher', models.CharField(max_length=33)),
                ('rent_cost', models.IntegerField()),
            ],
            options={
                'db_table': 'book',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DeliveryMan',
            fields=[
                ('lp_number', models.CharField(max_length=7, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=33)),
                ('vehicle_type', models.CharField(max_length=33)),
                ('availability_date', models.DateField()),
                ('phone', models.CharField(max_length=11)),
                ('provider_address', models.CharField(max_length=80)),
                ('recipient_address', models.CharField(max_length=80)),
            ],
            options={
                'db_table': 'delivery_man',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('t_id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('amount', models.IntegerField()),
            ],
            options={
                'db_table': 'payment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('nid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=11)),
                ('address', models.CharField(max_length=80)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=33)),
                ('fname', models.CharField(max_length=33)),
                ('lname', models.CharField(max_length=33)),
                ('age', models.IntegerField()),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Author',
            fields=[
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='library.book')),
                ('author_name', models.CharField(max_length=33)),
            ],
            options={
                'db_table': 'author',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RentProvider',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='library.user')),
            ],
            options={
                'db_table': 'rent_provider',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RentTaker',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='library.user')),
            ],
            options={
                'db_table': 'rent_taker',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Rents',
            fields=[
                ('rent_taker', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='library.renttaker')),
                ('rent_date', models.DateField()),
                ('rent_end_date', models.DateField()),
            ],
            options={
                'db_table': 'rents',
                'managed': False,
            },
        ),
    ]