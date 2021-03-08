# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from flectra.exceptions import ValidationError



class HrResignation(models.Model):
  _inherit="hr.resignation"


  loan_balance = fields.Float("Loan Balance", compute="_generate_balance_loan")
  comments = fields.Text(string="Comments")

  @api.onchange('employee_id')
  def set_join_date(self):
    var = super(HrResignation, self).set_join_date()
    # self.joined_date = self.employee_id.joining_date if self.employee_id.joining_date else ''
    if not self.joined_date:
      self.joined_date = self.employee_id.contract_id.date_start
      
      
  @api.multi
  @api.depends('employee_id')
  def _generate_balance_loan(self):
    for rec in self:
      loan_balance= 0.00
      loan_list = self.env['hr.loan'].search([('state','=','approve'),('employee_id','=',rec.employee_id.id),('balance_amount','>',0)])
      if loan_list:
        for loan in loan_list:
          loan_balance += loan.balance_amount
      self.loan_balance = loan_balance

  
  @api.multi
  def approve_resignation(self):
    for rec in self:
      if not rec.approved_revealing_date:
        raise ValidationError(_('Enter Approved Revealing Date'))
      if rec.approved_revealing_date and rec.resign_confirm_date:
        if rec.approved_revealing_date <= rec.resign_confirm_date:
          raise ValidationError(_('Approved revealing date must be anterior to confirmed date'))
        rec.state = 'approved'

    if rec.employee_id:
      employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id )])
      employee.write({
        'active':False,
      })
      contract = self.env['hr.contract'].search([('employee_id', '=', rec.employee_id.id)])
      contract.write({
        'state':'close',
      })




