from flectra.exceptions import ValidationError
from flectra import models, fields, api, _
from datetime import date, datetime,timedelta
import time

class holiinherit(models.Model):
    _inherit = 'hr.holidays'

    start_time = fields.Float('Start time')
    end_time = fields.Float('End Time')
    sli = fields.Boolean('short leave identifier', compute='_sli', default= False)

    @api.onchange('holiday_status_id')
    def _sli(self):
        for rec in self:
            if rec.holiday_status_id.name == 'Short Leave' or rec.holiday_status_id.name =='Half Day':
                rec.sli = True
                if rec.date_from:
                    
                    start_time = datetime.strptime(rec.date_from, '%Y-%m-%d %H:%M:%S')+ timedelta(hours=5,minutes=30)
                    start_time = start_time.time()
                    start_time = str(start_time).split(':')
                    
                    if float(start_time[1])*5/3 < 10.0:
                        k = '0'+ str(float(start_time[1])*5/3)
                    else:
                        k =str(float(start_time[1])*5/3)
                    
                    start_time = start_time[0]+'.'+ k
                    
                    start_time = str(start_time).split('.')
                    start_time = start_time[0]+'.'+start_time[1]
                    rec.start_time = start_time
            else:
                rec.sli = False
        
    @api.onchange('date_from')      
    def changetime(self):
        for rec in self:
            if rec.holiday_status_id.name == 'Short Leave' or rec.holiday_status_id.name =='Half Day':
            
                if rec.date_from:
                    
                    start_time = datetime.strptime(rec.date_from, '%Y-%m-%d %H:%M:%S')+ timedelta(hours=5,minutes=30)
                    start_time = start_time.time()
                    start_time = str(start_time).split(':')
                    
                    if float(start_time[1])*5/3 < 10.0:
                        k = '0'+ str(float(start_time[1])*5/3)
                    else:
                        k =str(float(start_time[1])*5/3)
                    
                    start_time = start_time[0]+'.'+ k
                    
                    start_time = str(start_time).split('.')
                    start_time = start_time[0]+'.'+start_time[1]
                    rec.start_time = start_time
            



    @api.model
    def create(self,vals):
        
        leave_type = vals['holiday_status_id']
        x =self.env['hr.holidays.status'].search([('id', '=', leave_type)],limit=1)
        if x.name == 'Short Leave' and vals['type'] == 'remove':


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

        if x.name == 'Half Day' and vals['type'] == 'remove':

            emp_id = vals['employee_id']
            employee = self.env['hr.employee'].search([('id', '=', emp_id)],limit=1)
            
            p = False
            
            for rec in employee.work_locat.half_day:
                st = rec.start_time
                et = rec.end_time

                if vals['start_time'] >= st and vals['start_time'] <= et:
                    p = True

            if p == False:
                raise ValidationError(_('This Time period is not allowed for half day of this employee.'))


        res = super(holiinherit, self).create(vals)
        return res 


