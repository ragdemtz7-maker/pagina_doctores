#!/bin/bash
set -e

OUTPUT_ZIP="front.zip"

echo "🧹 Limpiando ZIP anterior..."
rm -f "$OUTPUT_ZIP"

echo "📦 Creando ZIP desde carpeta front..."
cd front
zip -r "../$OUTPUT_ZIP" ./*
cd ..

echo "✅ ZIP generado: $OUTPUT_ZIP"
echo "👉 Sube este archivo a Amplify Hosting (manual deploy)."


