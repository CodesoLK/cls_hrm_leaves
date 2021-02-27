from flectra import models, fields, api, _

class worklocation(models.Model):
    _name = 'hr.work.location'

    name = fields.Char('Location Name')
    short_leave = fields.One2many('hr.short.leave','location_id',string = 'Short Leave Shifts')
    half_day = fields.One2many('hr.half.day','location_id', string= 'Half Day Shifts')

class shortLeave(models.Model):
    _name = 'hr.short.leave'

    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    location_id = fields.Many2one('hr.work.location', string = 'Location')

class halfDay(models.Model):
    _name = 'hr.half.day'

    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    location_id = fields.Many2one('hr.work.location', string = 'Location')

class holidayinherit(models.Model):
    _inherit = 'hr.employee'

    work_locat = fields.Many2one('hr.work.location',string='Work Location')

    guarentee_count_total = fields.Integer(string="Guarentee Count")


    # @api.one
    # def _get_guarentee_count_total(self):
        
    #     guarentee_one_count = self.env['hr.loan'].search_count([('guarantee_one', '=', self.id), ('state', '=', 'approve')
    #                                                 ])
    #     guarentee_two_count = self.env['hr.loan'].search_count([('guarantee_two', '=', self.id), ('state', '=', 'approve')
    #                                                    ])
    #     self.guarentee_count_total = guarentee_one_count + guarentee_two_count
