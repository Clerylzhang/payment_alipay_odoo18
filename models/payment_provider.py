# models/payment_provider.py
from odoo import models, fields, api

# 定义 PaymentProvider 类，继承自 payment.provider
class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    # 添加支付宝相关的字段
    code = fields.Selection(selection_add=[('alipay', 'Alipay')], ondelete={'alipay': 'set default'})
    alipay_app_id = fields.Char('Alipay 应用 ID', required_if_provider='alipay')
    alipay_api_key = fields.Char('Alipay API 密钥', required_if_provider='alipay')

    # 生成支付宝表单的值
    def _alipay_form_generate_values(self, values):
        alipay_values = dict(values)
        alipay_values.update({
            'app_id': self.alipay_app_id,
            'api_key': self.alipay_api_key,
        })
        return alipay_values

    # 获取支付宝支付的表单提交 URL
    def alipay_get_form_action_url(self):
        return 'https://openapi.alipay.com/gateway.do'