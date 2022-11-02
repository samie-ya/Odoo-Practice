"""This fine will craete the models for the realestate"""

from odoo import api,models,fields


class RealEstateType(models.Model):
  _name = "real.estate.type"
  _description = "What kind of House?"
  _order = "sequence, name"

  name = fields.Char(required=True)
  property_ids = fields.One2many('real.estate', 'type_id')
  sequence = fields.Integer()
  offer_ids = fields.One2many('real.estate.offers', 'property_type_id')
  offer_count = fields.Integer(compute='_count_offers')


  _sql_constraints = [('check_type_uniqueness', 'UNIQUE(name)', 'The name of a type should be unique')]

  @api.depends("offer_ids")
  def _count_offers(self):
    """This function will count the number of offers"""
    for record in self:
      record.offer_count = len(record.offer_ids.mapped('price'))
      
