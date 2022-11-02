"""This fine will craete the models for the realestate"""

from odoo import api,models,fields


class RealEstateTag(models.Model):
  _name = "real.estate.tag"
  _description = "How great is the house?"
  _order = "name asc"

  name = fields.Char(required=True)
  color = fields.Integer()



  _sql_constraints = [('check_unique_name', 'UNIQUE(name)', 'Name of the tag should be unique')]
