from odoo import models, fields, api
import requests
from datetime import datetime


class TraceabilityMedicamento(models.Model):
    _name = 'traceability.medicamento'
    _description = 'Trazabilidad de Medicamentos'

    product_id = fields.Many2one('product.product', string='Producto', required=True)
    lot_id = fields.Char(string='Lote', required=True)
    state = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('procesado', 'Procesado')
    ], string='Estado', default='pendiente')

    processing_date = fields.Date(string='Fecha de Procesamiento')
    processing_id = fields.Many2one('res.users', string='Procesado por', default=lambda self: self.env.user)

    @api.model
    def send_product_trazability(self):
        """
        Enviar productos pendientes a la API externa y actualizar su estado si es exitoso.
        """
        records = self.search([("state", "=", "pendiente")])

        for record in records:
            data = {
                "product": record.product_id.id,  # Enviar ID del producto
                "lot_id": record.lot_id,  # Lote como string
                "quantity": 1
            }

            try:
                response = requests.post("http://127.0.0.1:8000/procesar/", json=data)

                if response.status_code == 200:
                    result = response.json()  # Aquí estaba el error, faltaban los paréntesis
                    record.write({
                        "processing_id": self.env.user.id,  # Asignar el usuario actual
                        "processing_date": datetime.today().date(),
                        "state": "procesado"
                    })
                else:
                    raise models.ValidationError(f"Error en la API: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                raise models.ValidationError(f"Error en la conexión con la API: {e}")

    @api.model
    def update_product_trazability_status(self):
        """
        Actualizar el estado de los productos pendientes desde la API.
        """
        records = self.search([("state", "=", "pendiente")])

        for record in records:
            try:
                response = requests.get(f"http://127.0.0.1:8000/estado/{record.processing_id.id}")

                if response.status_code == 200:
                    data = response.json()
                    record.write({"state": data.get("status", record.state)})
                else:
                    raise models.ValidationError(f"Error en la API: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                raise models.ValidationError(f"Error en la conexión con la API: {e}")