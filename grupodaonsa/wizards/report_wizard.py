# -*- coding: utf-8 -*-

from odoo import models, fields, exceptions
from odoo.exceptions import UserError
import datetime, json
import pandas as pd

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
        var_create_data_document = self.create_data_document(data)
        #self.env['partner.pricelist'].create({
        #    'test': var_create_data_document,
        #    'pricelist': 1,
        #    'commission_percentage': 10
        #})
        raise exceptions.UserError(json.dumps(var_create_data_document, default=str))


    def create_data_document(self,data):
        creation_invoice, create_payment, payment_reference, amount_payment, payment_partner, invoice_name, age_date = [],[],[],[],[],[],[]
        amount_invoice, amount_subtotal, sale_team_invoice, vendor_invoice, price_list, subtotal_without_shipping, shipping = [],[],[],[],[],[],[]
        for d in data:
            creation_invoice.append(d['creation_invoice'])
            create_payment.append(d['create_payment'])
            payment_reference.append(d['payment_reference'])
            amount_payment.append(d['amount_payment'])
            payment_partner.append(d['payment_partner'])
            invoice_name.append(d['invoice_name'])
            age_date.append(d['age_date'])
            amount_invoice.append(d['amount_invoice'])
            amount_subtotal.append(d['amount_subtotal'])
            sale_team_invoice.append(d['sale_team_invoice'])
            vendor_invoice.append(d['vendor_invoice'])
            price_list.append(d['price_list'])
            subtotal_without_shipping.append(d['subtotal_without_shipping'])
            shipping.append(d['shipping'])
        df = pd.DataFrame({'Fecha factura': creation_invoice, 'Fecha de pago': create_payment, 'Referencia de pago': payment_reference,
            'Cantidad': amount_payment, 'Cliente': payment_partner, 'Factura': invoice_name, 'Antiguedad': age_date, 'Total factura': amount_invoice,
            'Subtotal factura': amount_subtotal, 'Equipo de ventas': sale_team_invoice, 'Vendedor': vendor_invoice, 'Lista de precios': price_list,
            'Subtotal sin envío': subtotal_without_shipping, 'Envío': shipping})
        return df

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
