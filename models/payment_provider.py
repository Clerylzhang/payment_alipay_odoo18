# models/payment_provider.py
from odoo import models, fields, api
from alipay import AliPay

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    # 添加支付宝相关的字段
    code = fields.Selection(selection_add=[('alipay', 'Alipay')], ondelete={'alipay': 'set default'})
    alipay_app_id = fields.Char('Alipay 应用 ID', required_if_provider='alipay')
    alipay_public_key = fields.Text('Alipay 公钥', required_if_provider='alipay')
    alipay_private_key = fields.Text('Alipay 私钥', required_if_provider='alipay')

    def _get_alipay_client(self):
        """获取支付宝客户端配置"""
        return AliPay(
            appid=self.alipay_app_id,
            app_notify_url=None,  # 默认回调 URL
            app_private_key_string=self.alipay_private_key,
            alipay_public_key_string=self.alipay_public_key,
            sign_type="RSA2",  # RSA 或 RSA2
            debug=False  # False 表示生产环境
        )

    # 生成支付宝表单的值
    def _alipay_form_generate_values(self, values):
        client = self._get_alipay_client()
        alipay_values = dict(values)
        alipay_values.update({
            'app_id': self.alipay_app_id,
        })
        return alipay_values

    # 获取支付宝支付的表单提交 URL
    def alipay_get_form_action_url(self):
        return 'https://openapi.alipay.com/gateway.do' if not self.test_mode else 'https://openapi.alipaydev.com/gateway.do'