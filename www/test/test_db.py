import os
import sys
parent_path = os.path.dirname(sys.path[0]) + '/transwarp'
parent_path1 = os.path.dirname(sys.path[0]) + '/'


if parent_path not in sys.path:
    sys.path.append(parent_path)
if parent_path1 not in sys.path:
    sys.path.append(parent_path1)

from models import User, Blog, Comment

from transwarp import db

db.create_engine(user='root', password='mysql', database='gbd_spider')

u = User(name='Test', email='test@example.com', password='1234567890', image='about:blank')

u.insert()

print 'new user id:', u.id

u1 = User.find_first('where email=?', 'test@example.com')
print 'find user\'s name:', u1.name

#u1.delete()

u2 = User.find_first('where email=?', 'test@example.com')
print 'find user:', u2