from flectra.exceptions import ValidationError
from flectra import models, fields, api, _

class holiinherit(models.Model):
    _inherit = 'hr.holidays'

    start_time = fields.Float('Start time')
    end_time = fields.Float('End Time')
    sli = fields.Boolean('short leave identifier', compute='_sli', default= False)

    @api.onchange('holiday_status_id')
    def _sli(self):
        for rec in self:
            if rec.holiday_status_id.name == 'Short Leave':
                rec.sli = True
            else:
                rec.sli = False


    @api.model
    def create(self,vals):
        
        leave_type = vals['holiday_status_id']
        x =self.env['hr.holidays.status'].search([('id', '=', leave_type)],limit=1)
        if x.name == 'Short Leave':


            emp_id = vals['employee_id']
            employee = self.env['hr.employee'].search([('id', '=', emp_id)],limit=1)
            
            p = False
            
            for rec in employee.work_locat.short_leave:
                st = rec.start_time
                et = rec.end_time

                if vals['start_time'] >= st and vals['start_time'] <= et:
                    p = True

            if p == False:
                raise ValidationError(_('This Time period is not allowed for short leaves of this employee.'))


        res = super(holiinherit, self).create(vals)
        return res 