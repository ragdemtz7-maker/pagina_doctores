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

# 5. Mostrar cuadro final con detalles del archivo
FILE="lambda_package.zip"
SIZE=$(du -h "$FILE" | cut -f1)
DATE=$(date +"%Y-%m-%d %H:%M:%S")

echo ""
echo "📊 Resumen del paquete generado"
echo "-----------------------------------------"
printf "📦 Nombre del archivo : %s\n" "$FILE"
printf "⚖️  Peso del archivo   : %s\n" "$SIZE"
printf "🕒 Fecha de creación   : %s\n" "$DATE"
echo "-----------------------------------------"

echo "✅ Paquete listo: $FILE"
echo "👉 Sube este archivo manualmente a AWS Lambda y configura el handler como:"
echo "   backend/app_swagger.handler"
