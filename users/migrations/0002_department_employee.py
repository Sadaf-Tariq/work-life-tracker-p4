# Generated by Django 3.2.22 on 2023-10-17 22:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('dept_ID', models.IntegerField(primary_key=True, serialize=False)),
                ('dept_name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('hired_on', models.DateTimeField()),
                ('joined_on', models.DateTimeField(auto_now_add=True)),
                ('work_email', models.EmailField(max_length=200, unique=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dept', to='users.department')),
            ],
            options={
                'ordering': ['hired_on'],
            },
        ),
    ]
