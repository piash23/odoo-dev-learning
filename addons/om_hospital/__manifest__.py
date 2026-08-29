{
    'name': 'OM Hospital',
    'version': '13.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Hospital Management',
    'summary': 'Hospital Management System',
    'description': """
        A comprehensive hospital management system to manage patients, doctors, appointments, and medical records.
    """,
    'author': 'Md Shihab Uddin',
    'website': 'https://www.example.com',
    'depends': ['base', 'mail', 'sale'],
    'data': [
        'security/hospital_security.xml',
        'security/ir.model.access.csv',
        
        'report/hospital_patient_report.xml',
        
        'data/hospital_sequence_data.xml',
        'data/hospital_patient_data.xml',
        'data/hospital_appointment_data.xml',

        'wizard/hospital_appointment_create_views.xml',

        'views/hospital_patient_views.xml',
        'views/sale_order_views.xml',
        'views/hospital_appointment_views.xml',
        'views/hospital_doctor_views.xml',
    ],
    'demo': [
        'demo/hospital_patient_demo.xml',
        'demo/hospital_doctor_demo.xml',
        'demo/hospital_appointment_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}