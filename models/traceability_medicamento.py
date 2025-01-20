from odoo import models, fields, api
import requests
from datetime import datetime


# Modelo que representa la trazabilidad de medicamentos
class TraceabilityMedicamento(models.Model):
    _name = 'traceability.medicamento'  
    _description = 'Trazabilidad de Medicamentos'  

    # Campos del modelo
    product_id = fields.Many2one('product.product', string='Producto', required=True)  
    lot_id = fields.Char(string='Lote', required=True) 
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado')
    ], string='Estado', default='pendiente')  
    processing_date = fields.Date(string='Fecha de Procesamiento')  
    processing_id = fields.Many2one('res.users', string='Procesado por', default=lambda self: self.env.user)  

    # Enviar la trazabilidad del producto a la API externa
    @api.model
    def send_product_trazability(self):
        records = self.search([("state", "=", "pendiente")])  

        for record in records:
            # Preparar datos para la API
            data = {
                "product": record.product_id.id,
                "lot_id": record.lot_id,
                "quantity": 1
            }

            try:
                # Realizar la petición POST a la API
                response = requests.post("http://127.0.0.1:8000/procesar/", json=data)

                if response.status_code == 200:
                    record.write({
                        "processing_id": self.env.user.id,
                        "processing_date": datetime.today().date(),
                        "state": "procesado"
                    })
                else:
                    raise models.ValidationError(f"Error en la API: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                raise models.ValidationError(f"Error en la conexión con la API: {e}")

    # Actualizar el estado del medicamento desde la API
    @api.model
    def update_product_trazability_status(self):
        records = self.search([("state", "=", "pendiente")])  # Buscar registros pendientes

        for record in records:
            try:
                # Realizar la petición GET a la API
                response = requests.get(f"http://127.0.0.1:8000/estado/{record.processing_id.id}")

                if response.status_code == 200:
                    data = response.json()
                    record.write({"state": data.get("status", record.state)})
                else:
                    raise models.ValidationError(f"Error en la API: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                raise models.ValidationError(f"Error en la conexión con la API: {e}")
