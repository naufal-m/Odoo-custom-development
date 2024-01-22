# below dictionary gives under app module info.
{
    'name': 'OM Hospital',
    'author': 'OM Hospital Teams',
    'website': 'www.odoomates.tech',
    'summary': 'Odoo 16 Development for Hospital management module',
    # adding the inheriting module folder name into the depends.
    'depends': ['sale',
                'mail'
                ],
    # call all folder files here under the module folder
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'wizard/create_appointment_view.xml',
        'wizard/view_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/patient_gender_view.xml',
        'views/kids_view.xml',
        'views/sale.xml',
        'views/appointment_view.xml',
        'views/appointment_view.xml',
        'views/doctor_view.xml',
        'views/department_view.xml',
        'report/report.xml',
        'report/patient_card.xml',
    ]
}
