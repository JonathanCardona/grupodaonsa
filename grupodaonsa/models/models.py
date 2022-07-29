# -*- coding: utf-8 -*-


from odoo import models, fields


class PartnerPricelist(models.Model):
    _name = 'partner.pricelist'


    pricelist = fields.Many2one('product.pricelist', string='Lista de precio', required=True, change_default=True, index=True)
    commission_percentage = fields.Float('Porcentaje de comision')
    test = fields.Text('ejemplos')

