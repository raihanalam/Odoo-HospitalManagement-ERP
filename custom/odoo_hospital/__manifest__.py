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
    'depends': ['account', 'sale', 'mail', 'report_xlsx', 'board'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/data.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'wizards/create_appointment.xml',
        'views/appointment.xml',
        'views/patient.xml',
        'views/doctor.xml',
        'views/manager.xml',
        'views/lab.xml',
        'views/settings.xml',
        'views/dashboard.xml',
        'views/template.xml',
        'views/sale_order.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
        'reports/sale_report_inherit.xml',
        'reports/appointment.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}