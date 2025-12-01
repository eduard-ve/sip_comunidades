#!/usr/bin/env python
"""
Script para verificar que los tests del backend están pasando
"""

import subprocess
import sys
import os

def run_backend_tests():
    """Ejecutar solo los tests específicos que estaban fallando"""
    
    # Cambiar al directorio backend
    os.chdir('backend')
    
    # Tests específicos que estaban fallando
    test_cases = [
        'apps/usuarios/tests.py::TestFormValidations::test_registro_serializer_duplicate_email',
        'apps/usuarios/tests.py::TestErrorHandling::test_perfil_update_invalid_data',
        'apps/usuarios/tests.py::TestErrorHandling::test_usuario_delete_nonexistent',
        'apps/encuestas/tests.py::TestFormValidations::test_pregunta_form_validation_opcion_multiple_no_opciones'
    ]
    
    print("🧪 Verificando los tests específicos del backend...")
    print("=" * 60)
    
    all_passed = True
    
    for test in test_cases:
        print(f"\n🔍 Ejecutando: {test}")
        try:
            result = subprocess.run([
                sys.executable, '-m', 'pytest', test, '-v'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ PASSED")
            else:
                print(f"❌ FAILED")
                print("STDOUT:", result.stdout)
                print("STDERR:", result.stderr)
                all_passed = False
                
        except subprocess.TimeoutExpired:
            print(f"⏰ TIMEOUT")
            all_passed = False
        except Exception as e:
            print(f"💥 ERROR: {e}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡TODOS LOS TESTS DEL BACKEND ESTÁN PASANDO!")
    else:
        print("⚠️  Algunos tests fallaron")
    
    return all_passed

if __name__ == "__main__":
    run_backend_tests()