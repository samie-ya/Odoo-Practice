"""This file will compute the wage of different job titles"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class JobWage(models.Model):
  _inherit="hr.job"

  maximum_wage = fields.Float(required=True, copy=False)
  minimum_wage = fields.Float(required=True, copy=False)

  _sql_constraints = [
                      ('check_on_maximum_wage', 'CHECK(maximum_wage > 0 AND maximum_wage > minimum_wage)', 'Maximum wage must be more than Minimum Wage and 0'),
                      ('check_on_minimum_wage', 'CHECK(minimum_wage > 0 AND minimum_wage < maximum_wage)', 'Minimum wage must be less than Maximum Wage and greater than 0')
                     ]

class JobWageCheck(models.Model):
  _inherit="hr.contract"

  @api.model
  def create(self, vals):
      """This function will check whether wage is within range"""
      position = self.env['hr.job'].browse(vals['job_id'])
      if (vals['wage'] < position.minimum_wage):
        Message = "Wage must be more than the company Minimum wage scale of " + str(position.minimum_wage)
        raise UserError(_(Message))
      elif (vals['wage'] > position.maximum_wage):
        Message = "Wage must be less than the company Maximum wage scale of " + str(position.maximum_wage)
        raise UserError(_(Message))
      else:
        return super(JobWageCheck, self).create(vals)
