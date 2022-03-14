import os


def main():
    os.system('docker-compose build')
    os.system('docker-compose run web django-admin startproject config .')
    os.system('sudo chmod -R 777 *')
    which_programs()

def which_programs():
    list_of_apps = [app for app in input("Type your apps (Example: user client cart): ").split() if app != "end!"]
    os.system('mkdir apps')
    for app in list_of_apps:
        os.system('cd apps && mkdir {}'.format(app))
    os.system('sudo chmod -R 777 *')
    for app in list_of_apps:
        os.system('docker-compose run web python3 manage.py startapp {} apps/{}'.format(str(app), str(app)))
    settings_installed_apps(list_of_apps)
    create_folder_in_apps(list_of_apps)

def settings_installed_apps(somelist):
    somelist = somelist.copy()
    string = [f"\n\t'apps.{app}'," for app in somelist]
    another = "".join(string)
    another += "\n\t'rest_framework',"
    with open('config/settings.py', 'r') as client:
        a = client.read()

    with open('config/settings.py', 'w') as client:
        from_letter = a.find("'django.contrib.staticfiles',")
        count = len("'django.contrib.staticfiles',")
        client.write(a[0:from_letter + count] + another + a[from_letter + count:])

def create_folder_in_apps(list_of_apps):
    for app in list_of_apps:
        os.system('sudo chmod -R 777 *')
        removing_files(app)
        append_apps_in_apps_py(app)
        os.system('cd apps/{} && mkdir models && mkdir serializers && mkdir tests && mkdir views'.format(app))
        os.system('sudo chmod -R 777 *')
        create_files_inside_folders(app)

def removing_files(app):
    os.remove(f'apps/{app}/models.py')
    os.remove(f'apps/{app}/tests.py')
    os.remove(f'apps/{app}/views.py')

def append_apps_in_apps_py(app):
    with open(f'apps/{app}/apps.py', 'r') as client:
        a = client.read()
        
    from_letter = a.find(app)
    with open(f'apps/{app}/apps.py', 'w') as client:
        client.write(a[0:from_letter] + "apps." + a[from_letter:])

def create_files_inside_folders(app):
    with open(f'apps/{app}/models/{app}.py', 'w') as model:
        model.write('''from django.db import models


class {}(models.Model):
    pass

    def __str__(self):
        return self.field     # <-------

    class Meta:
        verbose_name = '{}'     # <-------
        verbose_name = '{}s'    # <-------
'''.format(str(app).capitalize(), app, app))
    with open(f'apps/{app}/models/__init__.py', 'w') as model:
        model.write('''from apps.{}.models.{} import {}'''.format(app, app, str(app).capitalize()))
    with open(f'apps/{app}/serializers/{app}.py', 'w') as serializers:
        serializers.write('''from rest_framework import serializers
from apps.{}.models.{} import {}


class {}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {}
        fields = '__all__'
'''.format(app, app, str(app).capitalize(), str(app).capitalize(), str(app).capitalize()))
    with open(f'apps/{app}/views/{app}.py', 'w') as views:
        views.write('''from rest_framework.views import APIView
from apps.{}.models.{} import {}
from apps.{}.serializers.{} import {}Serializer


class {}View(APIView):
    pass
'''.format(app, app, str(app).capitalize(), app, app, str(app).capitalize(), str(app).capitalize()))
    with open(f'apps/{app}/tests/test_model.py', 'w') as test_model:
        test_model.write('''from django.test import TestCase


class {}ModelTest(TestCase):
    pass
'''.format(str(app).capitalize()))

    with open(f'apps/{app}/tests/test_serializers.py', 'w') as test_serializers:
        test_serializers.write('''from django.test import TestCase


class {}SerializerTest(TestCase):
    pass
'''.format(str(app).capitalize()))
    
    with open(f'apps/{app}/tests/test_views.py', 'w') as test_views:
        test_views.write('''from django.test import TestCase


class {}ViewTest(TestCase):
    pass
'''.format(str(app).capitalize()))
        
        
if __name__ == "__main__":
    main()
