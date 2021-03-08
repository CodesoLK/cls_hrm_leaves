# -*- coding: utf-8 -*-

from flectra import models, fields, api, _
from flectra.exceptions import ValidationError
# class openacademy(models.Model):
#     _name = 'openacademy.openacademy'

#     name = fields.Char()

#inheriting model
class LoanAttributesModification(models.Model):
    _inherit = 'hr.loan'
    guarantee_one = fields.Many2one('hr.employee', string="Guarantee One", domain=[('guarentee_count_total', '<',2 )])
    guarantee_two = fields.Many2one('hr.employee', string="Guarantee Two",  domain=[('guarentee_count_total', '<', 2)])
    
    transfered_loan = fields.Boolean('Transfered Loan', default=False)

    state = fields.Selection(selection_add=[('finish', 'Finished')])


    
    
    @api.model
    def create(self,vals):

        if vals['employee_id'] == vals['guarantee_one'] or vals['employee_id'] == vals['guarantee_two']:
            raise ValidationError('Employee Can not Guarantee for his/her own loan')

        employee =vals['guarantee_one']
        emp = self.env['hr.employee'].search([('id', '=', employee)],limit=1)
        emp_guarantee_count = emp.guarentee_count_total
        emp_guarantee_count += 1
        emp.write({'guarentee_count_total':emp_guarantee_count})

        employee =vals['guarantee_two']
        emp = self.env['hr.employee'].search([('id', '=', employee)],limit=1)
        emp_guarantee_count = emp.guarentee_count_total
        emp_guarantee_count += 1
        emp.write({'guarentee_count_total':emp_guarantee_count})

        result = super(LoanAttributesModification,self).create(vals)
        return result

    @api.multi
    def unlink(self):

        employee =self.guarantee_one
        emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
        emp_guarantee_count = emp.guarentee_count_total
        emp_guarantee_count -= 1
        emp.write({'guarentee_count_total':emp_guarantee_count})

        employee =self.guarantee_two
        emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
        emp_guarantee_count = emp.guarentee_count_total
        emp_guarantee_count -= 1
        emp.write({'guarentee_count_total':emp_guarantee_count})

        result = super(LoanAttributesModification,self).unlink()
        return result

    @api.multi
    def write(self,vals):

        if self.state == 'approve':
            if vals['state'] == 'finish':
                employee =self.guarantee_one
                emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
                emp_guarantee_count = emp.guarentee_count_total
                emp_guarantee_count -= 1
                emp.write({'guarentee_count_total':emp_guarantee_count})

                employee =self.guarantee_two
                emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
                emp_guarantee_count = emp.guarentee_count_total
                emp_guarantee_count -= 1
                emp.write({'guarentee_count_total':emp_guarantee_count})

        if vals['state'] == 'refuse':
            employee =self.guarantee_one
            emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
            emp_guarantee_count = emp.guarentee_count_total
            emp_guarantee_count -= 1
            emp.write({'guarentee_count_total':emp_guarantee_count})

            employee =self.guarantee_two
            emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
            emp_guarantee_count = emp.guarentee_count_total
            emp_guarantee_count -= 1
            emp.write({'guarentee_count_total':emp_guarantee_count})

        
        if vals['state'] == 'cancel':
            employee =self.guarantee_one
            emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
            emp_guarantee_count = emp.guarentee_count_total
            emp_guarantee_count -= 1
            emp.write({'guarentee_count_total':emp_guarantee_count})

            employee =self.guarantee_two
            emp = self.env['hr.employee'].search([('id', '=', employee.id)],limit=1)
            emp_guarantee_count = emp.guarentee_count_total
            emp_guarantee_count -= 1
            emp.write({'guarentee_count_total':emp_guarantee_count})

        result = super(LoanAttributesModification,self).write(vals)
        return result

    def loan_transfer_to_the_guarantee(self):
        self.ensure_one()
        pending_installments = self.env['hr.loan.line'].search_count([('loan_id','=',self.id),('paid','=',False)])
        
        return {
            'name': _('Loan Transfer'),
            'type': 'ir.actions.act_window',            
            'res_model': 'loan.transfer.guarantee.wizard',
            'view_mode': 'form',
            'view_type' : 'form',
            
            'context': dict(
                self.env.context,
                default_employee_id=self.employee_id.id,
                default_pending_amount=self.balance_amount,
                default_no_of_installments=pending_installments,
                default_guarantee_one=self.guarantee_one.id,
                default_guarantee_two=self.guarantee_two.id,
                default_loan_id=self.id,
                
            ),
            'target'    : 'new',
        }

    @api.onchange('guarantee_one')
    def onchange_gurantee_1(self):
        return {
        'domain' : {'guarantee_two' : [('id', '!=', self.guarantee_one.id),('guarentee_count_total', '<',2 )],}
        }
  
    @api.onchange('guarantee_two')
    def onchange_gurantee_2(self):
        return {
        'domain' : {'guarantee_one' : [('id', '!=', self.guarantee_one.id),('guarentee_count_total', '<',2 )],}
        }
  