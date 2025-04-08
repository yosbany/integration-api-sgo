#!/bin/bash

# Colores para la salida
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Iniciando pruebas de la API de Zureo...${NC}"

# Verificar si existe el archivo .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}Archivo .env no encontrado. Creando desde test.env.example...${NC}"
    if [ -f test.env.example ]; then
        cp test.env.example .env
        echo -e "${YELLOW}Por favor, edita el archivo .env con tus credenciales antes de continuar.${NC}"
        exit 1
    else
        echo -e "${RED}Error: No se encontró test.env.example${NC}"
        exit 1
    fi
fi

# Instalar dependencias si es necesario
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creando entorno virtual...${NC}"
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ejecutar los tests
echo -e "${YELLOW}Ejecutando tests...${NC}"
python test_client.py

# Capturar el código de salida
TEST_RESULT=$?

# Mostrar resultado
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}Todos los tests pasaron exitosamente.${NC}"
else
    echo -e "${RED}Algunos tests fallaron. Revisa los detalles arriba.${NC}"
fi

# Desactivar el entorno virtual
deactivate

exit $TEST_RESULT 