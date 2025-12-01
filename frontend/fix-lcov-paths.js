import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Leer el archivo LCOV original
const lcovPath = path.join(__dirname, 'coverage', 'lcov.info');

try {
  let content = fs.readFileSync(lcovPath, 'utf8');

  // Reemplazar todos los paths que empiezan con 'src/' o 'src\' por 'frontend/src/'
  content = content.replace(/^SF:src[\/\\]/gm, 'SF:frontend/src/');

  // Escribir el archivo corregido sobre el original
  fs.writeFileSync(lcovPath, content, 'utf8');

  console.log('✅ Archivo LCOV corregido exitosamente');
  console.log('   Paths actualizados: src/ -> frontend/src/');
} catch (error) {
  console.error('❌ Error al corregir archivo LCOV:', error.message);
  process.exit(1);
}