#!/bin/bash

# Obtener el directorio donde está este script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "==============================="
echo "   Iniciando PedalCuad...      "
echo "==============================="

# Activar el entorno virtual si existe
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Ejecutar el frontend
python3 source/frontend/pedalcuad

# Mantener la terminal abierta si hay un error para poder leerlo
if [ $? -ne 0 ]; then
    echo " "
    echo "⚠️ Hubo un error al ejecutar PedalCuad."
    read -p "Presiona Enter para salir..."
fi
