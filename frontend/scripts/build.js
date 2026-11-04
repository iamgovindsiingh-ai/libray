import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const frontendDir = path.resolve(__dirname, '..');
const backendStaticDir = path.resolve(frontendDir, '../backend/app/static/react');
const distDir = path.resolve(frontendDir, 'dist');

// 1. Run Vite Build
console.log('[Build] Compiling React frontend with Vite...');
execSync('npx vite build', { stdio: 'inherit', cwd: frontendDir });

// 2. Copy compiled static files to frontend/dist for Capacitor
console.log('[Build] Mirroring assets to frontend/dist for Capacitor...');
if (fs.existsSync(backendStaticDir)) {
  fs.mkdirSync(distDir, { recursive: true });
  fs.cpSync(backendStaticDir, distDir, { recursive: true });
  console.log('[Build] Successfully mirrored assets to frontend/dist!');
} else {
  console.error(`[Build Error] Backend static directory not found: ${backendStaticDir}`);
  process.exit(1);
}
