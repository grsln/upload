#!/bin/sh
# python manage.py flush --no-input
python manage.py migrate --no-input
python manage.py collectstatic --no-input
python manage.py shell -c "from django.contrib.auth.hashers import make_password; from django.contrib.auth import get_user_model; MyUser = get_user_model(); MyUser.objects.filter( username__exact = 'admin' ).count() == 0 or exit(); new_super_user = MyUser( username = 'admin', email='email@example.com', is_superuser = True, is_staff = True ); new_super_user.password = make_password('admin'); new_super_user.save();"
exec "$@"
