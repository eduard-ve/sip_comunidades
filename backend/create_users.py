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
        print(f'✓ Superusuario creado: {admin.username} (password: admin123)')

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
        print(f'✓ Usuario editor creado: {editor.username} (password: editor123)')

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
        print(f'✓ Usuario invitado creado: {invitado.username} (password: invitado123)')

    print('\nCredenciales de prueba:')
    print('=' * 40)
    print('Admin:     admin / admin123')
    print('Editor:    editor / editor123')
    print('Invitado:  invitado / invitado123')
    print('=' * 40)

if __name__ == '__main__':
    create_test_users()