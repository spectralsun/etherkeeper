# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Pad', fields ['title_author']
        #db.delete_unique(u'etherpad_pad', ['title_author_id'])

        # Removing unique constraint on 'Invite', fields ['pad']
        #db.delete_unique(u'etherpad_invite', ['pad_id'])

        # Removing unique constraint on 'Invite', fields ['to']
        #db.delete_unique(u'etherpad_invite', ['to_id'])

        # Removing unique constraint on 'Invite', fields ['sender']
        #db.delete_unique(u'etherpad_invite', ['sender_id'])

        # Removing unique constraint on 'PadMember', fields ['pad']
        #db.delete_unique(u'etherpad_padmember', ['pad_id'])


        # Changing field 'PadMember.pad'
        #db.alter_column(u'etherpad_padmember', 'pad_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpad.Pad']))

        # Changing field 'Invite.sender'
        #db.alter_column(u'etherpad_invite', 'sender_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Author']))

        # Changing field 'Invite.to'
        #db.alter_column(u'etherpad_invite', 'to_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Author']))

        # Changing field 'Invite.pad'
        #db.alter_column(u'etherpad_invite', 'pad_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['etherpad.Pad']))

        # Changing field 'Pad.title_author'
        #db.alter_column(u'etherpad_pad', 'title_author_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Author'], null=True))

    def backwards(self, orm):

        # Changing field 'PadMember.pad'
        db.alter_column(u'etherpad_padmember', 'pad_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['etherpad.Pad'], unique=True))
        # Adding unique constraint on 'PadMember', fields ['pad']
        db.create_unique(u'etherpad_padmember', ['pad_id'])


        # Changing field 'Invite.sender'
        db.alter_column(u'etherpad_invite', 'sender_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['core.Author']))
        # Adding unique constraint on 'Invite', fields ['sender']
        db.create_unique(u'etherpad_invite', ['sender_id'])


        # Changing field 'Invite.to'
        db.alter_column(u'etherpad_invite', 'to_id', self.gf('django.db.models.fields.related.OneToOneField')(unique=True, to=orm['core.Author']))
        # Adding unique constraint on 'Invite', fields ['to']
        db.create_unique(u'etherpad_invite', ['to_id'])


        # Changing field 'Invite.pad'
        db.alter_column(u'etherpad_invite', 'pad_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['etherpad.Pad'], unique=True))
        # Adding unique constraint on 'Invite', fields ['pad']
        db.create_unique(u'etherpad_invite', ['pad_id'])


        # Changing field 'Pad.title_author'
        db.alter_column(u'etherpad_pad', 'title_author_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.Author'], unique=True, null=True))
        # Adding unique constraint on 'Pad', fields ['title_author']
        db.create_unique(u'etherpad_pad', ['title_author_id'])


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
        u'etherpad.invite': {
            'Meta': {'object_name': 'Invite'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pad': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['etherpad.Pad']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_invites'", 'to': u"orm['core.Author']"}),
            'sent': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invites'", 'to': u"orm['core.Author']"})
        },
        u'etherpad.pad': {
            'Meta': {'object_name': 'Pad'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'groupid': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'padid': ('django.db.models.fields.CharField', [], {'max_length': '42'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'title_author': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Author']", 'null': 'True'}),
            'title_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        },
        u'etherpad.padmember': {
            'Meta': {'object_name': 'PadMember'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pads'", 'null': 'True', 'to': u"orm['core.Author']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 1, 25, 0, 0)'}),
            'pad': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'members'", 'to': u"orm['etherpad.Pad']"}),
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