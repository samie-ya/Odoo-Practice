"""Ths function will create a base model for estate property"""

from odoo import fields, models, api
from odoo.exceptions import AccessError

class RealEstateAccount(models.Model):
  _inherit = "real.estate"


  def sold_or_not_sold(self):
    invoice_cut_offs = (self.selling_price * 0.06) + 100.00
    journal = self.env['account.journal'].search([('type', '=', 'sale')])
    self.env['account.move'].create({
      'partner_id': self.buyer.id,
      'move_type': 'out_invoice',
      'journal_id': journal.id,
      'invoice_line_ids': [
        (
          0,
          0,
          {
            'name': self.description,
            'quantity': 1.0,
            'price_unit': self.selling_price
          }
        ),
        (
          0,
          0,
          {
            'name': self.description,
            'quantity': 1.0,
            'price_unit': invoice_cut_offs
          }
        )
      ]
    })
    return super(RealEstateAccount, self).sold_or_not_sold()
