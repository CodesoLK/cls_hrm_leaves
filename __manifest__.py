{
    'name': 'HRM Leaves Leaf',
    'version': '1.0',
    'author' : 'Thisura Weerakkody',
    'category': 'Extra tools',
    'sequence': '38',
    'summary': 'FOR HRM of Ceylon Leaf Springs Leaves Process',
    'depends': [ 'base','hr','hr_holidays','hr_resignation'],
                 
    'data': [
            'views/work_location.xml',
            'views/employee.xml',
            'views/leaves.xml',
            'views/document.xml',
            'views/hr_resignation.xml',
            'views/hr_loan.xml',
            'wizard/loan_transfer_to_guarantees.xml',

                               
    ],
    'demo': [],

'installable': True,
'application': True,
'auto_install': False,
}