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
        
        'report/hospital_patient_report.xml',
        
        'data/hospital_sequence_data.xml',
        'data/hospital_patient_data.xml',
        'data/hospital_appointment_data.xml',

        'views/hospital_patient_views.xml',
        'views/sale_order_views.xml',
        'views/hospital_appointment_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}