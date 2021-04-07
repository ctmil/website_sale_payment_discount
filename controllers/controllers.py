# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging
_logger = logging.getLogger(__name__)

class WebsiteSalePaymentDiscount(WebsiteSale):
	@http.route(['/shop/update_payment'], type='json', auth='public', methods=['POST'], website=True, csrf=False)
	def update_eshop_payment(self, **post):
		results = {}
		self._add_website_sale_payment(**post)
		results = self._update_website_sale_payment(**post)
		return results

	def _update_website_sale_payment(self, **post):
		order = request.website.sale_get_order()
		payment_id = int(post['payment_id'])
		currency = order.currency_id
		discount = request.env['payment.acquirer'].sudo().search([('id', '=', payment_id)])
		amount_discount = (discount.discount * order.amount_total) / 100
		order.payment_id = payment_id
		order.payment_discount = amount_discount * -1

		return {
                       	'status': True,
                       	'new_amount_untaxed': self._format_amount(order.amount_untaxed + order.payment_discount, currency),
                       	'new_amount_tax': self._format_amount(order.amount_tax, currency),
                       	'new_amount_total': self._format_amount(order.amount_total + order.payment_discount, currency),
                       	'discount': self._format_amount(order.payment_discount, currency),
		}

	def _add_website_sale_payment(self, **post):
		order = request.website.sale_get_order()
		payment_id = int(post['payment_id'])
		currency = order.currency_id
		discount = request.env['payment.acquirer'].sudo().search([('id', '=', payment_id)])
		amount_discount = (discount.discount * order.amount_total) / 100
		order.payment_id = payment_id
		order.payment_discount = amount_discount * -1

		if discount.product_discount:

			sale = request.env['sale.order.line'].sudo().create({
                           'product_id': discount.product_discount.id,
                           'name': 'Descuento por Método de Pago',
                           'product_uom_qty': 1,
                           'price_unit': amount_discount * -1,
                           'order_id': order.id,
                           'customer_lead': 0
			})


