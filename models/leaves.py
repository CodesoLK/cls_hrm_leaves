from flectra import models, fields, api, _

class worklocation(models.Model):
    _name = 'hr.work.location'

    name = fields.Char('Location Name')
    short_leave = fields.One2many('hr.short.leave','location_id',string = 'Short Leave Shifts')


class shortLeave(models.Model):
    _name = 'hr.short.leave'

    start_time = fields.Float('Start Time')
    end_time = fields.Float('End Time')
    location_id = fields.Many2one('hr.work.location', string = 'Location')

class holidayinherit(models.Model):
    _inherit = 'hr.employee'

    work_locat = fields.Many2one('hr.work.location',string='Work Location')
