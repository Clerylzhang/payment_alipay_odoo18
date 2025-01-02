# controllers/main.py
from odoo import http
from odoo.http import request

# 定义 AlipayController 类，继承自 http.Controller
class AlipayController(http.Controller):
    # 定义路由来处理支付宝支付返回
    @http.route(['/payment/alipay/return'], type='http', auth='public', csrf=False)
    def alipay_return(self, **post):
        # 处理支付宝支付反馈
        request.env['payment.transaction'].sudo().form_feedback(post, 'alipay')
        return request.redirect('/payment/process')