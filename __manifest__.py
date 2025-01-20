{
    'name': 'Medicamentos',
    'version': '1.0',
    'category': 'Inventory',
    'summary': 'Gestión de trazabilidad de medicamentos',
    'description': 'Este módulo gestiona la trazabilidad de medicamentos en el sistema.',
    'author': 'Tu Nombre',
    'depends': ['base', 'stock', 'product'],
    'data': [
    'security/ir.model.access.csv',
    'views/traceability_views.xml',
],
    'installable': True,
    'application': True,
}