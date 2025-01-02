# controllers/main.py
from odoo import http
from odoo.http import request
import logging
from alipay import AliPay

_logger = logging.getLogger(__name__)

class AlipayController(http.Controller):
    @http.route(['/payment/alipay/return'], type='http', auth='public', csrf=False)
    def alipay_return(self, **post):
        _logger.info("Received Alipay return: %s", post)
        try:
            request.env['payment.transaction'].sudo().form_feedback(post, 'alipay')
            return request.redirect('/payment/process')
        except Exception as e:
            _logger.error("Error processing Alipay return: %s", e)
            return request.redirect('/payment/error')

    @http.route(['/payment/alipay/pay'], type='http', auth='public', csrf=False)
    def alipay_pay(self, **kwargs):
        provider = request.env['payment.provider'].search([('code', '=', 'alipay')], limit=1)
        if not provider:
            return "Alipay provider not found"

        client = provider._get_alipay_client()
        order_string = client.api_alipay_trade_page_pay(
            out_trade_no="unique_order_id",
            total_amount=kwargs.get("amount"),  # 支付金额
            subject=kwargs.get("subject"),  # 订单标题
            return_url="https://yourdomain.com/payment/alipay/return"
        )

        payment_url = 'https://openapi.alipay.com/gateway.do?' + order_string
        return request.redirect(payment_url)