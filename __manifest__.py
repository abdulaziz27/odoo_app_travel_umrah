# -*- coding: utf-8 -*-
{
    'name': 'Travel Umroh',
    'summary': """Management Travel Umroh""",
    'description': 'Modul ini berfungsi untuk memanage semua proses yang ada pada jasa Travel Umroh',
    'author': '@ad_dulziz - 0852 1155 3430',
    'website': "https://www.dulganzz.blogspot.com",
    'category': "Industries",
    'version': '12.1',
    'depends': ['base', 'mail', 'sale', 'account', 'uom'],
    'data': [
        'report/print_deliveryorder.xml',
        'report/print_invoice.xml',
        'security/ir.model.access.csv',
        'views/templates.xml',
        'views/views.xml',
        'report/report_suratjalan.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
