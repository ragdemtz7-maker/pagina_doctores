#!/bin/bash
set -e

# 🚀 Script de despliegue manual para FastAPI + Mangum en AWS Lambda

# 1. Limpiar build anterior
echo "🧹 Limpiando carpeta build..."
rm -rf build
mkdir build

# 2. Copiar backend
echo "📂 Copiando backend..."
cp -r backend build/

# 3. Instalar dependencias en build
echo "📦 Instalando dependencias..."
pip install -r backend/requirements.txt -t build/ --upgrade --force-reinstall

# 4. Crear ZIP
echo "🗜️ Empaquetando en lambda_package.zip..."
cd build
zip -r9 ../lambda_package.zip .
cd ..

echo "✅ Paquete listo: lambda_package.zip"
echo "👉 Sube este archivo manualmente a AWS Lambda y configura el handler como:"
echo "   backend/app_swagger.handler"
