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
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/hospital_patient_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}