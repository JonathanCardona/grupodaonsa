# -*- coding: utf-8 -*-


from odoo import models, fields,api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    customer_key = fields.Char(string='Clave de cliente', compute='_default_clave_cliente', store=True)

    @api.depends('x_studio_clave_cliente') 
    def _default_clave_cliente(self):
        for record in self:
            if 'x_studio_clave_cliente' in self.env['res.partner']._fields:
                str_x_studio_clave_cliente = f'{record.x_studio_clave_cliente:06d}'
            else:
                str_x_studio_clave_cliente = '0'
            record.customer_key = str_x_studio_clave_cliente
