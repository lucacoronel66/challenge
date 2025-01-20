# Traceability Medicamento

Este módulo para **Odoo 16 Community** gestiona la trazabilidad de medicamentos, integrando los sistemas de compras y ventas con un sistema externo a través de una API. Su objetivo es facilitar la sincronización de productos trazados y la consulta del estado de los envíos.

## Características

- Gestión de productos trazables.
- Sincronización con un sistema externo para procesar la trazabilidad de medicamentos.
- Actualización del estado de los productos procesados.
- Implementación de un mock del sistema externo con FastAPI.

## Requisitos previos

1. Tener **Odoo 16 Community** instalado y configurado.
2. Python 3.8+ con los siguientes paquetes instalados:
   - `fastapi`
   - `uvicorn`
   - `pydantic`
3. Conexión a internet para realizar pruebas con la API.

## Instalación

1. **Clonar el repositorio**:
    ```bash
    git clone https://github.com/lucacoronel66/challenge.git
    ```

2. **Copiar el módulo al directorio de Odoo**:
    ```bash
    cp -r challenge_odoo/traceability_medicamento /path/to/odoo/addons/
    ```

3. **Actualizar la lista de aplicaciones en Odoo**:
    - Accede a Odoo como administrador.
    - Navega a `Aplicaciones` y haz clic en `Actualizar lista de aplicaciones`.

4. **Instalar el módulo**:
    - Busca "Trazabilidad de Medicamentos" en la lista de aplicaciones.
    - Haz clic en `Instalar`.

## Configuración de la API externa

El módulo se integra con un sistema externo simulado mediante FastAPI. Puedes ejecutar este sistema en local para probar las funcionalidades del módulo.

### Pasos para ejecutar la API mock:

1. **Instalar dependencias**:
    ```bash
    pip install fastapi uvicorn pydantic
    ```

2. **Ejecutar el servidor de FastAPI**:
    ```bash
    uvicorn api:app --reload --host 127.0.0.1 --port 8000
    ```

   Esto inicia el servidor en `http://127.0.0.1:8000`.

### Endpoints disponibles:

1. **Procesar un medicamento**:
    - URL: `POST /procesar/`
    - Ejemplo de payload:
      ```json
      {
          "product_id": 1,
          "lot_id": "L123",
          "quantity": 10
      }
      ```

2. **Consultar el estado de procesamiento**:
    - URL: `GET /estado/{processing_id}`
    - Ejemplo de respuesta:
      ```json
      {
          "processing_id": "abc123",
          "status": "procesado",
          "message": "El Medicamento fue procesado correctamente"
      }
      ```

## Uso del módulo

### Registro de trazabilidad
1. Navega al menú `Inventario > Trazabilidad de Medicamentos`.
2. Haz clic en `Crear` y registra un producto, lote y estado inicial.
3. Usa el botón `Enviar a la API` para sincronizar con el sistema externo.

### Actualización del estado
1. Desde la vista de lista, puedes consultar los registros pendientes y procesados.
2. Usa la función de actualización para sincronizar el estado desde la API externa.

## Propuesta de mejoras

1. **Validación avanzada**:
    - Agregar validaciones para asegurar que solo se procesen productos válidos.
2. **Notificaciones**:
    - Enviar notificaciones al usuario cuando un procesamiento sea exitoso o falle.
3. **Lista de Medicamentos validos y disponibles**:
    - Se debe de listar medicamentos validos y disponibles al usuario.