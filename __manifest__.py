{
    'name': 'Payment Alipay Odoo18',
    'version': '1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Payment Acquirer Integration for Alipay in Odoo 18',
    'description': """
        This module integrates Alipay payment gateway with Odoo 18, allowing businesses to accept payments
        through Alipay directly within their Odoo platform.
    """,
    'author': 'Clerylzhang',
    'license': 'AGPL-3',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_templates.xml',  # 支付模板视图
        'data/payment_provider_data.xml',  # 支付供应商数据
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/icon.png'],
}
