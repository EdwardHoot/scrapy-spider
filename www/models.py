#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Models for user, tasks, task_running_log.
'''

import time, uuid

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class User(Model):
    __table__ = 'users'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    email = StringField(updatable=False, ddl='varchar(50)')
    password = StringField(ddl='varchar(50)')
    admin = BooleanField()
    name = StringField(ddl='varchar(50)')
    image = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)
    updated_at = FloatField(updatable=True, default=time.time)


class Task(Model):
    __table__ = 'tasks'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    user_id = StringField(updatable=False, ddl='varchar(50)')
    task_status = StringField(ddl='varchar(1)')
    task_name = StringField(ddl='varchar(50)')
    start_time = FloatField(updatable=False, default=time.time)
    end_time = FloatField(updatable=True)
    description = StringField(ddl='varchar(200)')
    created_at = FloatField(updatable=False, default=time.time)
    created_by = StringField(ddl='varchar(50)')
    updated_at = FloatField(updatable=True, default=time.time)
    updated_by = StringField(ddl='varchar(50)')


class TaskRunningLog(Model):
    __table__ = 'task_running_log'

    id = StringField(primary_key=True, default=next_id, ddl='varchar(50)')
    task_id = StringField(updatable=False, ddl='varchar(50)')
    running_task_status = StringField(updatable=True, ddl='varchar(1)')
    description = StringField(ddl='varchar(500)')
    created_at = FloatField(updatable=False, default=time.time)
    created_by = StringField(ddl='varchar(50)')
    updated_at = FloatField(updatable=True, default=time.time)
    updated_by = StringField(ddl='varchar(50)')
