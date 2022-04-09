{
    'name': 'Hospital Management',
    'version': '15.0',
    'category': 'Extra Tools',
    'summary': 'Module for managing the Hospitals',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': 'Raihan Alam',
    'maintainer': 'Raihan',
    'website': 'emargenhospital.com',
    'depends': ['account', 'sale'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/appointment.xml',
        'views/patient.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}