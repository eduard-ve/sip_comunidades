#!/usr/bin/env python
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip.settings')
django.setup()

from django.contrib.auth import get_user_model

Usuario = get_user_model()

def create_test_users():
    # Crear superusuario
    if not Usuario.objects.filter(username='admin').exists():
        admin = Usuario.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Administrador',
            last_name='Sistema',
            rol='admin'
        )
        print(f'[OK] Superusuario creado: {admin.username} (password: admin123)')

    # Crear usuario editor
    if not Usuario.objects.filter(username='editor').exists():
        editor = Usuario.objects.create_user(
            username='editor',
            email='editor@example.com',
            password='editor123',
            first_name='Editor',
            last_name='Sistema',
            rol='editor'
        )
        print(f'[OK] Usuario editor creado: {editor.username} (password: editor123)')

    # Crear usuario invitado
    if not Usuario.objects.filter(username='invitado').exists():
        invitado = Usuario.objects.create_user(
            username='invitado',
            email='invitado@example.com',
            password='invitado123',
            first_name='Invitado',
            last_name='Sistema',
            rol='invitado'
        )
        print(f'[OK] Usuario invitado creado: {invitado.username} (password: invitado123)')

    # Crear usuario admin2
    if not Usuario.objects.filter(username='admin2').exists():
        admin2 = Usuario.objects.create_superuser(
            username='admin2',
            email='admin2@example.com',
            password='123456',
            first_name='Administrador',
            last_name='Secundario',
            rol='admin'
        )
        print(f'[OK] Superusuario admin2 creado: {admin2.username} (password: 123456)')

    print('\nCredenciales de prueba:')
    print('=' * 40)
    print('Admin:     admin / admin123')
    print('Admin2:    admin2 / 123456')
    print('Editor:    editor / editor123')
    print('Invitado:  invitado / invitado123')
    print('=' * 40)

if __name__ == '__main__':
    create_test_users()