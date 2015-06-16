# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessEntity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('filename', models.CharField(max_length=64)),
                ('attached_file', models.FileField(upload_to=b'attachments')),
                ('mimetype', models.CharField(max_length=64, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ConfigSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('value', models.TextField(null=True, blank=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('accessentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AccessEntity')),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(null=True, blank=True)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='core.Group', null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.accessentity',),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=75)),
                ('key', models.CharField(max_length=256)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('default_group', models.ForeignKey(blank=True, to='core.Group', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ModuleSetting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('label', models.CharField(max_length=512)),
                ('value', models.TextField()),
                ('group', models.ForeignKey(blank=True, to='core.Group', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_name', models.CharField(max_length=512, null=True, blank=True)),
                ('object_type', models.CharField(max_length=512, null=True, blank=True)),
                ('trash', models.BooleanField(default=False)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('nuvius_resource', models.TextField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('details', models.TextField(blank=True)),
                ('url', models.CharField(max_length=512)),
                ('display', models.BooleanField(default=True)),
                ('system', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=512)),
                ('parent', models.ForeignKey(related_name='child_set', blank=True, to='core.Location', null=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('title', models.CharField(max_length=256)),
                ('body', models.TextField(blank=True)),
                ('published', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='PageFolder',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(blank=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Perspective',
            fields=[
                ('object_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.Object')),
                ('name', models.CharField(max_length=256)),
                ('details', models.TextField(blank=True)),
                ('modules', models.ManyToManyField(to='core.Module', null=True, blank=True)),
            ],
            options={
            },
            bases=('core.object',),
        ),
        migrations.CreateModel(
            name='Revision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('change_type', models.CharField(max_length=512, null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('object', models.ForeignKey(to='core.Object')),
                ('previous', models.OneToOneField(related_name='next', null=True, blank=True, to='core.Revision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RevisionField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('field_type', models.CharField(max_length=512, null=True, blank=True)),
                ('field', models.CharField(max_length=512, null=True, blank=True)),
                ('value', models.TextField(null=True, blank=True)),
                ('revision', models.ForeignKey(to='core.Revision')),
                ('value_key', models.ForeignKey(related_name='revisionfield_key', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Object', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=512)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UpdateRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('record_type', models.CharField(max_length=32, choices=[(b'create', b'create'), (b'update', b'update'), (b'delete', b'delete'), (b'trash', b'trash'), (b'message', b'message'), (b'manual', b'manual'), (b'share', b'share')])),
                ('url', models.CharField(max_length=512, null=True, blank=True)),
                ('body', models.TextField(default=b'', null=True, blank=True)),
                ('score', models.IntegerField(default=0)),
                ('format_message', models.TextField(null=True, blank=True)),
                ('format_strings', models.TextField(null=True, blank=True)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
                ('about', models.ManyToManyField(related_name='updates', null=True, to='core.Object', blank=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('accessentity_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='core.AccessEntity')),
                ('name', models.CharField(max_length=256)),
                ('disabled', models.BooleanField(default=False)),
                ('last_access', models.DateTimeField(default=datetime.datetime.now)),
                ('default_group', models.ForeignKey(related_name='default_user_set', blank=True, to='core.Group', null=True)),
                ('other_groups', models.ManyToManyField(to='core.Group', null=True, blank=True)),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('core.accessentity',),
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('module_name', models.CharField(max_length=256)),
                ('widget_name', models.CharField(max_length=256)),
                ('weight', models.IntegerField(default=0)),
                ('perspective', models.ForeignKey(to='core.Perspective')),
                ('user', models.ForeignKey(to='core.User')),
            ],
            options={
                'ordering': ['weight'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='author',
            field=models.ForeignKey(related_name='sent_updates', blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='comments',
            field=models.ManyToManyField(related_name='comments_on_updates', null=True, to='core.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='dislikes',
            field=models.ManyToManyField(related_name='updates_disliked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='likes',
            field=models.ManyToManyField(related_name='updates_liked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='recipients',
            field=models.ManyToManyField(related_name='received_updates', null=True, to='core.AccessEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='updaterecord',
            name='sender',
            field=models.ForeignKey(related_name='sent_updates', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.Object', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revisionfield',
            name='value_key_acc',
            field=models.ForeignKey(related_name='revisionfield_key_acc', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.AccessEntity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revisionfield',
            name='value_m2m',
            field=models.ManyToManyField(related_name='revisionfield_m2m', to='core.Object'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='revisionfield',
            name='value_m2m_acc',
            field=models.ManyToManyField(related_name='revisionfield_m2m_acc', to='core.AccessEntity'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='folder',
            field=models.ForeignKey(to='core.PageFolder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='comments',
            field=models.ManyToManyField(related_name='comments', null=True, to='core.Comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='creator',
            field=models.ForeignKey(related_name='objects_created', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='dislikes',
            field=models.ManyToManyField(related_name='objects_disliked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='full_access',
            field=models.ManyToManyField(related_name='objects_full_access', null=True, to='core.AccessEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='likes',
            field=models.ManyToManyField(related_name='objects_liked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='links',
            field=models.ManyToManyField(related_name='links_rel_+', null=True, to='core.Object', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='read_access',
            field=models.ManyToManyField(related_name='objects_read_access', null=True, to='core.AccessEntity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='subscribers',
            field=models.ManyToManyField(related_name='subscriptions', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='object',
            name='tags',
            field=models.ManyToManyField(to='core.Tag', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modulesetting',
            name='module',
            field=models.ForeignKey(blank=True, to='core.Module', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modulesetting',
            name='perspective',
            field=models.ForeignKey(blank=True, to='core.Perspective', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='modulesetting',
            name='user',
            field=models.ForeignKey(blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invitation',
            name='sender',
            field=models.ForeignKey(blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(blank=True, to='core.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='dislikes',
            field=models.ManyToManyField(related_name='comments_disliked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='likes',
            field=models.ManyToManyField(related_name='comments_liked', null=True, to='core.User', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='attached_object',
            field=models.ForeignKey(blank=True, to='core.Object', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='attached_record',
            field=models.ForeignKey(blank=True, to='core.UpdateRecord', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attachment',
            name='uploaded_by',
            field=models.ForeignKey(to='core.User'),
            preserve_default=True,
        ),
    ]
