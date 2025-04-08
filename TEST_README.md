# Cliente de Pruebas para la API de Zureo

Este cliente automatizado permite probar todos los endpoints de la API de Zureo desplegada en Render.

## Características

- Prueba automática de todos los endpoints
- Formato de salida claro y visual
- Resumen de resultados
- Configuración mediante variables de entorno
- Script de ejecución automatizado

## Requisitos

- Python 3.8+
- pip (Python package manager)
- Bash (para ejecutar el script)

## Configuración

1. Copia el archivo de ejemplo de variables de entorno:
   ```bash
   cp test.env.example .env
   ```

2. Edita el archivo `.env` con tus credenciales:
   ```
   ZUREO_EMAIL=tu_email@ejemplo.com
   ZUREO_PASSWORD=tu_password
   TEST_SKU=SKU_DE_PRUEBA
   TEST_QUANTITY=10
   ```

## Ejecución

### Usando el script automatizado

```bash
./run_tests.sh
```

El script:
1. Verifica si existe el archivo `.env`
2. Crea un entorno virtual si es necesario
3. Instala las dependencias
4. Ejecuta los tests
5. Muestra un resumen de los resultados

### Ejecución manual

```bash
# Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python test_client.py
```

## Endpoints probados

1. **Health Check** (`GET /`)
   - Verifica que la API esté funcionando

2. **Login** (`POST /zureo/login`)
   - Prueba el inicio de sesión con las credenciales proporcionadas

3. **Get Stock** (`GET /zureo/stock/{sku}`)
   - Verifica la consulta de stock para un SKU específico

4. **Adjust Stock** (`GET /zureo/ajustar/{sku}/{cantidad}`)
   - Prueba el ajuste de stock para un SKU específico

## Interpretación de resultados

- ✅ PASS: El test pasó correctamente
- ❌ FAIL: El test falló

Al final se muestra un resumen con el resultado de todos los tests.

## Códigos de salida

- 0: Todos los tests pasaron
- 1: Al menos un test falló

## Solución de problemas

Si encuentras errores:

1. Verifica que las credenciales en `.env` sean correctas
2. Asegúrate de que la API esté funcionando en Render
3. Revisa los mensajes de error para identificar el problema específico
4. Verifica que el SKU de prueba exista en el sistema 