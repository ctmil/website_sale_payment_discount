# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PaymentAcquier(models.Model):
    _inherit = 'payment.acquirer'

    discount = fields.Float('Descuento')
    product_discount = fields.Many2one('product.product', 'Producto del Descuento')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    payment_discount = fields.Float('Descuento por Método de Pago', default=0)
    payment_id = fields.Many2one('payment.acquirer', 'Método de Pago')

class ProductProduct(models.Model):
    _inherit = 'product.product'

    is_payment = fields.Boolean('Es Método de Pago')
