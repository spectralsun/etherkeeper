# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'PadAuthor'
        db.delete_table(u'etherpad_padauthor')

        # Removing M2M table for field tags on 'PadAuthor'
        db.delete_table(db.shorten_name(u'etherpad_padauthor_tags'))

        # Adding model 'PadMember'
        db.create_table(u'etherpad_padmember', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pad', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['etherpad.Pad'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Author'], null=True)),
        ))
        db.send_create_signal(u'etherpad', ['PadMember'])

        # Adding M2M table for field tags on 'PadMember'
        m2m_table_name = db.shorten_name(u'etherpad_padmember_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('padmember', models.ForeignKey(orm[u'etherpad.padmember'], null=False)),
            ('tag', models.ForeignKey(orm[u'organize.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['padmember_id', 'tag_id'])


    def backwards(self, orm):
        # Adding model 'PadAuthor'
        db.create_table(u'etherpad_padauthor', (
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Author'], null=True)),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('pad', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['etherpad.Pad'], unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'etherpad', ['PadAuthor'])

        # Adding M2M table for field tags on 'PadAuthor'
        m2m_table_name = db.shorten_name(u'etherpad_padauthor_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('padauthor', models.ForeignKey(orm[u'etherpad.padauthor'], null=False)),
            ('tag', models.ForeignKey(orm[u'organize.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['padauthor_id', 'tag_id'])

        # Deleting model 'PadMember'
        db.delete_table(u'etherpad_padmember')

        # Removing M2M table for field tags on 'PadMember'
        db.delete_table(db.shorten_name(u'etherpad_padmember_tags'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.author': {
            'Meta': {'object_name': 'Author'},
            'etherpad_id': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'etherpad.pad': {
            'Meta': {'object_name': 'Pad'},
            'created': ('django.db.models.fields.DateField', [], {}),
            'groupid': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'padid': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'etherpad.padmember': {
            'Meta': {'object_name': 'PadMember'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Author']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pad': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['etherpad.Pad']", 'unique': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['organize.Tag']", 'symmetrical': 'False'})
        },
        u'organize.tag': {
            'Meta': {'object_name': 'Tag'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Author']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['etherpad']