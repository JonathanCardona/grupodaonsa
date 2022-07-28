# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions
from odoo.exceptions import UserError
import datetime, json

class ReportWizard(models.TransientModel):
    _name = 'report.wizard'
    _description = 'Report Wizard'

    month = fields.Selection([
        ('01', 'Enero'),
        ('02', 'Febrero'),
        ('03', 'Marzo'),
        ('04', 'Abril'),
        ('05', 'Mayo'),
        ('06', 'Junio'),
        ('07', 'Julio'),
        ('08', 'Agosto'),
        ('09', 'Septiembre'),
        ('10', 'Octubre'),
        ('11', 'Noviembre'),
        ('12', 'Diciembre')
    ],string="Mes")

    trimester = fields.Selection([
        ('first_trimester', 'Enero-Febrero-Marzo'),
        ('second_trimester', 'Abril-Mayo-Junio'),
        ('third_trimester', 'Julio-Agosto-Septiembre'),
        ('fourth_trimester', 'Octubre-Noviembre-Diciembre')
    ], string="Trimestre")


    def generate_report(self):
        payments = self.env['account.payment'].search([('state', '=', 'posted')])
        data = []
        for p in payments:
            invoice = self.get_invoice(p)
            month_invoice = format(p.create_date.month, '02')
            if self.month == month_invoice:
                age_date = self.calculate_age(p, invoice)

                shipping_price = self.get_shipping_price(invoice)
                subtotal_without_shipping = invoice.amount_untaxed - shipping_price
                dict = {"creation_invoice": invoice.create_date,"create_payment": p.create_date, "payment_reference": p.ref,
                    "amount_payment": p.amount,"payment_partner": p.partner_id.name, "invoice_name": p.ref, "age_date": age_date,
                    "amount_invoice": invoice.amount_total,"amount_subtotal": invoice.amount_untaxed,
                    "sale_team_invoice": p.move_id.team_id.name, "vendor_invoice": p.move_id.invoice_user_id.name,
                    "price_list": p.move_id.partner_id.property_product_pricelist.name, "subtotal_without_shipping": subtotal_without_shipping,
                    "shipping": shipping_price}
                data.append(dict)
        raise exceptions.UserError(json.dumps(data, default=str))


    def get_invoice(self, payment):
        return self.env['account.move'].search([('name', '=', payment.ref)])

    def calculate_age(self, payment, invoice):
        return (payment.create_date.date() - invoice.create_date.date()).days

    def get_shipping_price(self, invoice):
        invoice_lines = self.env['account.move.line'].search([('move_id', '=', invoice.id)])
        if invoice_lines:
            for i in invoice_lines:
                if i.product_id.categ_id.name == 'Envios':
                    shipping_price = i.price_unit
                else:
                    shipping_price = 0.0
                return shipping_price
