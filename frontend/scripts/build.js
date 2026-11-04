import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const backendStaticDir = path.resolve(frontendDir, '../backend/app/static/react');
const distDir = path.resolve(frontendDir, 'dist');
const androidAssetsDir = path.resolve(frontendDir, 'android/app/src/main/assets');
const androidPublicDir = path.resolve(androidAssetsDir, 'public');
const capConfigFile = path.resolve(frontendDir, 'capacitor.config.json');

// 1. Run Vite Build
console.log('[Build] Compiling React frontend with Vite...');
execSync('npx vite build', { stdio: 'inherit', cwd: frontendDir });

// 2. Mirror to frontend/dist
console.log('[Build] Mirroring assets to frontend/dist...');
if (fs.existsSync(backendStaticDir)) {
  fs.mkdirSync(distDir, { recursive: true });
  fs.cpSync(backendStaticDir, distDir, { recursive: true });
  console.log('[Build] Successfully mirrored assets to frontend/dist!');
}

// 3. Mirror directly into native Android assets
console.log('[Build] Mirroring assets directly into Android native app assets...');
fs.mkdirSync(androidPublicDir, { recursive: true });
fs.cpSync(backendStaticDir, androidPublicDir, { recursive: true });

if (fs.existsSync(capConfigFile)) {
  fs.copyFileSync(capConfigFile, path.join(androidAssetsDir, 'capacitor.config.json'));
}
console.log('[Build] Native Android assets ready for Gradle compilation!');
