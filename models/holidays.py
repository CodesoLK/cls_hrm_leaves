from flectra.exceptions import ValidationError
from flectra import models, fields, api, _
from datetime import date, datetime,timedelta
import time

class holiinherit(models.Model):
    _inherit = 'hr.holidays'

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    start_time = fields.Float('Start time')
    end_time = fields.Float('End Time')
    sli = fields.Boolean('short leave identifier', compute='_sli', default= False)
    employee_id = fields.Many2one('hr.employee', string='Employee', index=True, readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, default=_default_employee, track_visibility='onchange')
    epf = fields.Char('Epf NO', compute='get_epf', readonly=True)
    shift = fields.Selection([('m', 'Morning'), ('a', 'Afternoon'), ('e', 'Evening')],
                             string='Time Shift')
    short = fields.Boolean('Short Leave Only', compute='short_leave', default= False)

    @api.onchange('shift')
    def onchange_shift(self):
        if self.holiday_status_id.name == 'Short Leave':
            employee = self.env['hr.employee'].search([('id', '=', self.employee_id.id)]) 
            if employee.work_locat:
                shifts=[]
                for x in employee.work_locat.short_leave:
                    shifts.append(x)
                shift1 = shifts[0].start_time
                shift2 = shifts[1].start_time
                shift3 = shifts[2].start_time
                
                convert_time1 = '{0:02.0f}:{1:02.0f}'.format(*divmod(shift1 * 60, 60))
                convert_time2 = '{0:02.0f}:{1:02.0f}'.format(*divmod(shift2 * 60, 60))
                convert_time3 = '{0:02.0f}:{1:02.0f}'.format(*divmod(shift3 * 60, 60))

                standard_format1 = convert_time1 + ':' + '00'
                standard_format2 = convert_time2 + ':' + '00'
                standard_format3 = convert_time3 + ':' + '00'

                datetime1 = str(datetime.today().date())+ ' ' + str(standard_format1)
                datetime1 = datetime.strptime(datetime1,'%Y-%m-%d %H:%M:%S')
                std_datetime1 = datetime1 -timedelta(hours=5,minutes=30)
                
                datetime2 = str(datetime.today().date())+ ' ' + str(standard_format2)
                datetime2 = datetime.strptime(datetime2,'%Y-%m-%d %H:%M:%S')
                std_datetime2 = datetime2 -timedelta(hours=5,minutes=30)

                datetime3 = str(datetime.today().date())+ ' ' + str(standard_format3)
                datetime3 = datetime.strptime(datetime3,'%Y-%m-%d %H:%M:%S')
                std_datetime3 = datetime3 -timedelta(hours=5,minutes=30)
                
                datetimex= str(datetime.today().date()) +' '+ '23:59:00'
                datetimex =datetime.strptime(datetimex,'%Y-%m-%d %H:%M:%S')
                std_datetimex = datetimex -timedelta(hours=5,minutes=30)
                self.date_to = std_datetimex
                self.number_of_days_temp = 1

                if self.shift == 'm':
                    self.date_from = std_datetime1
                    

                elif self.shift == 'a':
                    self.date_from = std_datetime2

                else:
                    self.date_from = std_datetime3

                
               
            



        

    @api.onchange('holiday_status_id')
    def short_leave(self):
        for rec in self:
            if rec.holiday_status_id.name == 'Short Leave':
                rec.short = True
            else:
                rec.short = False


    def get_epf(self):
        for rec in self:
            if rec.employee_id:
                employee = self.env['hr.employee'].search([('id', '=', rec.employee_id.id)])
                rec.epf = employee.epf_no

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


