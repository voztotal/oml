# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 15:38
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_agente', models.BooleanField(default=False)),
                ('is_customer', models.BooleanField(default=False)),
                ('is_supervisor', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AgenteProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sip_extension', models.IntegerField(unique=True)),
                ('sip_password', models.CharField(blank=True, max_length=128, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('name', models.CharField(max_length=128, primary_key=True, serialize=False)),
                ('timeout', models.BigIntegerField()),
                ('retry', models.BigIntegerField()),
                ('maxlen', models.BigIntegerField()),
                ('wrapuptime', models.BigIntegerField()),
                ('servicelevel', models.BigIntegerField()),
                ('strategy', models.CharField(choices=[('ringall', 'Ringall'), ('roundrobin', 'Roundrobin'), ('leastrecent', 'Leastrecent'), ('fewestcalls', 'Fewestcalls'), ('random', 'Random'), ('rrmemory', 'Rremory')], max_length=128)),
                ('eventmemberstatus', models.BooleanField()),
                ('eventwhencalled', models.BooleanField()),
                ('weight', models.BigIntegerField()),
                ('ringinuse', models.BooleanField()),
                ('setinterfacevar', models.BooleanField()),
                ('musiconhold', models.CharField(blank=True, max_length=128, null=True)),
                ('announce', models.CharField(blank=True, max_length=128, null=True)),
                ('context', models.CharField(blank=True, max_length=128, null=True)),
                ('monitor_join', models.NullBooleanField()),
                ('monitor_format', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_youarenext', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_thereare', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_callswaiting', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_holdtime', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_minutes', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_seconds', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_lessthan', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_thankyou', models.CharField(blank=True, max_length=128, null=True)),
                ('queue_reporthold', models.CharField(blank=True, max_length=128, null=True)),
                ('announce_frequency', models.BigIntegerField(blank=True, null=True)),
                ('announce_round_seconds', models.BigIntegerField(blank=True, null=True)),
                ('announce_holdtime', models.CharField(blank=True, max_length=128, null=True)),
                ('joinempty', models.CharField(blank=True, max_length=128, null=True)),
                ('leavewhenempty', models.CharField(blank=True, max_length=128, null=True)),
                ('reportholdtime', models.NullBooleanField()),
                ('memberdelay', models.BigIntegerField(blank=True, null=True)),
                ('timeoutrestart', models.NullBooleanField()),
            ],
            options={
                'db_table': 'queue_table',
            },
        ),
        migrations.CreateModel(
            name='QueueMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membername', models.CharField(max_length=128)),
                ('interface', models.CharField(max_length=128)),
                ('penalty', models.IntegerField(choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9')])),
                ('paused', models.IntegerField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.AgenteProfile')),
                ('queue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.Queue')),
            ],
            options={
                'db_table': 'queue_member_table',
            },
        ),
        migrations.AddField(
            model_name='queue',
            name='members',
            field=models.ManyToManyField(through='ominicontacto_app.QueueMember', to='ominicontacto_app.AgenteProfile'),
        ),
        migrations.AddField(
            model_name='agenteprofile',
            name='grupo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ominicontacto_app.Grupo'),
        ),
        migrations.AddField(
            model_name='agenteprofile',
            name='modulos',
            field=models.ManyToManyField(to='ominicontacto_app.Modulo'),
        ),
        migrations.AddField(
            model_name='agenteprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='queuemember',
            unique_together=set([('queue', 'membername')]),
        ),
    ]
