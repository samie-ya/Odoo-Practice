"""This class will create inheritance"""

from odoo import api, models, fields


class RealEstateUsers(models.Model):
  _inherit="res.users"

  property_ids = fields.One2many('real.estate', 'seller')
