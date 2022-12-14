"""This fine will craete the models for the realestate"""

from odoo import api,models,fields, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class RealEstateOffers(models.Model):
  _name = "real.estate.offers"
  _description = "How much did we get?"
  _order = "price desc"

  price = fields.Float()
  status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('rejected', 'Rejected')])
  partner_id = fields.Many2one('res.partner', required=True)
  property_id = fields.Many2one('real.estate', required=True)
  validity = fields.Integer(default=7)
  date_deadline = fields.Datetime(compute="_compute_deadline", inverse="_inverse_deadline")
  property_type_id = fields.Many2one(related="property_id.type_id", store=True)

  _sql_constraints = [('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive')]


  @api.model
  def create(self, vals):
    """This function will make modificatiosn to created of offer"""
    property = self.env['real.estate'].browse(vals['property_id'])
    price_lists = property.offer_ids.mapped('price')
    if price_lists != []:
      least_offer = sorted(price_lists)
      if vals['price'] <= least_offer[0]:
        raise UserError(_('You can not create an offer that is lower than the prices given.'))
      else:
        property.state = 'offer received'
    else:
      property.state = 'offer received'
    return super(models.Model, self).create(vals)


  def offer_confirm(self):
    """This function will confirm an offer"""
    for record in self:
      record.property_id.selling_price = record.price
      record.property_id.buyer = record.partner_id
      record.status = 'accepted'
      record.property_id.state = 'offer accepted'

  def offer_cancel(self):
    """This function will cancel an offer"""
    for record in self:
      record.status = 'rejected'

  def _inverse_deadline(self):
    """thsi function will allow the editing of the values"""
    for record in self:
      if record.date_deadline:
        days = (record.date_deadline - record.create_date).days
        record.validity = int(days)

  @api.depends('validity', 'create_date')
  def _compute_deadline(self):
    """This function will compute the deadline for an offer"""
    for record in self:
      if record.create_date:
        record.date_deadline = record.create_date + timedelta(days=record.validity)
      else:
        record.date_deadline = ''
