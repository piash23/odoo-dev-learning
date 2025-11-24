{
    'name': 'OM Hospital',
    'version': '1.0',
    'category': 'Hospital Management',
    'summary': 'Hospital Management System',
    'description': """
        A comprehensive hospital management system to manage patients, doctors, appointments, and medical records.
    """,
    'author': 'Md Shihab Uddin',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail', 'sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/hospital_sequence_data.xml',
        'views/hospital_patient_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}