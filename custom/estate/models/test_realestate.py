"""This creates a model real estate for file"""


from odoo import models, fields,api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError
from odoo.tools.float_utils import float_compare

class RealEstate(models.Model):
  _name="real.estate"
  _description="let's make houses"
  _order = "id desc"

  name = fields.Char(required=True)
  description = fields.Char()
  postcode = fields.Char()
  date_availability = fields.Date(copy=False, default =datetime.now() + timedelta(days=90))
  expected_price = fields.Float(required=True)
  selling_price = fields.Float(copy=False, readonly=True)
  bedrooms = fields.Integer(default=2)
  living_areas = fields.Integer()
  facades = fields.Integer()
  garage = fields.Boolean()
  garden = fields.Boolean()
  garden_area = fields.Integer()
  garden_orientation = fields.Selection(string="Garden Orientation", selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')])
  active = fields.Boolean('Active', default=True)
  type_id = fields.Many2one('real.estate.type', string="Property Type")
  seller = fields.Many2one('res.users', string="Seller", default=lambda self: self.env.user)
  buyer = fields.Many2one('res.partner', copy=False, string="Buyer")
  tag_ids = fields.Many2many('real.estate.tag', string="Tags")
  offer_ids = fields.One2many('real.estate.offers', 'property_id')
  state = fields.Selection(string="State", selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')], required=True, copy=False, default='new')
  total_area = fields.Integer(compute='_compute_total_area')
  best_price = fields.Float(compute='_compute_best_price')


  _sql_constraints = [('check_expected_prce', 'CHECK(expected_price > 0)', 'Expected Price must be Positive'),
                      ('check_selling_price', 'CHECK(selling_price >= 0)', 'Selling Price must be Positive')
                     ]

  def unlink(self):
    """This function will delete only new and cancelled records"""
    for record in self:
      if record.state == 'new' or record.state == 'cancelled':
        return super(RealEstate, self).unlink()
      else:
        raise UserError(_('You can not delete a record that is not new nor cancelled'))

  @api.constrains('expected_price')
  def _contrain_selling_price(self):
    """This function will create a constrain on the selling price"""
    for record in self:
      if record.selling_price > 0:
        price = record.expected_price * 0.9
        compare = float_compare(record.selling_price, price, precision_digits=2)
        if compare == -1:
          raise ValidationError(_('The selling price must be atleast 90% of expected price. You must reduce your expected price if you want to accept this offer'))

  def sold_or_not_sold(self):
    """This function checks whether a property is sold or not"""
    for record in self:
      if record.state == 'sold':
        raise UserError(_('An already sold property can not be resold'))
      elif record.state == 'cancelled':
        raise UserError(_('Property is already cancelled'))
      else:
        record.state = 'sold'
   
  def cancelled_or_not_cancelled(self):
    """This function will check whetehr a property has been cancelled or not"""
    for record in self:
      if record.state == 'sold':
        raise UserError(_('An already sold property can not be cancelled'))
      elif record.state == 'cancelled':
        raise UserError(_('Property is already cancelled'))
      else:
        record.state = 'cancelled'

  @api.onchange('garden')
  def _change_based_on_garden(self):
    """This function will toggle fields based on garden"""
    for record in self:
      if record.garden:
        record.garden_area = 10
        record.garden_orientation = 'north'
      else:
        record.garden_area = 0
        record.garden_orientation = ''

  @api.depends('offer_ids')
  def _compute_best_price(self):
    """This function will compute the best price form offers"""
    for record in self:
      if record.offer_ids:
        price = record.offer_ids.mapped('price')
        highest = sorted(price)
        record.best_price = highest[-1]
      else:
        record.best_price = 0
  
  @api.depends('garden_area', 'living_areas')
  def _compute_total_area(self):
    """This function will get the total area of the house"""
    for record in self:
      record.total_area = record.living_areas + record.garden_area
