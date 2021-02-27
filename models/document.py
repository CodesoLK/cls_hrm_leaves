from datetime import datetime, date, timedelta
from flectra import models, fields, api, _
from flectra.exceptions import Warning


class HRDocument(models.Model):
    _name = 'hr.document'
    _description = 'HR Documents'

    
    @api.constrains('expiry_date')
    def check_expr_date(self):
        for each in self:
            if each.expiry_date:
                exp_date = fields.Date.from_string(each.expiry_date)
                if exp_date < date.today():
                    raise Warning('Your Document Is Expired.')

    name = fields.Char(string='Document Number', required=True, copy=False, help='You can give your'
                                                                                 'Document number.')
    
    description = fields.Text(string='Description', copy=False)
    expiry_date = fields.Date(string='Expiry Date', copy=False)
    # employee_ref = fields.Many2one('op.student', invisible=1, copy=False)
    doc_attachment_id = fields.Many2many('ir.attachment', 'doc_attach_rel_n', 'doc_id', 'attach_id3', string="Attachment",
                                         help='You can attach the copy of your document', copy=False)
    issue_date = fields.Date(string='Issue Date', default=fields.datetime.now(), copy=False)


# class OpStudents(models.Model):
#     _inherit = 'op.student'

#     @api.multi
#     def _document_count(self):
#         for each in self:
#             document_ids = self.env['op.student.document'].sudo().search([('employee_ref', '=', each.id)])
#             each.document_count = len(document_ids)

#     @api.multi
#     def document_view(self):
#         self.ensure_one()
#         domain = [
#             ('employee_ref', '=', self.id)]
#         return {
#             'name': _('Documents'),
#             'domain': domain,
#             'res_model': 'op.student.document',
#             'type': 'ir.actions.act_window',
#             'view_id': False,
#             'view_mode': 'tree,form',
#             'view_type': 'form',
#             'help': _('''<p class="oe_view_nocontent_create">
#                            Click to Create for New Documents
#                         </p>'''),
#             'limit': 80,
#             'context': "{'default_employee_ref': '%s'}" % self.id
#         }

#     document_count = fields.Integer(compute='_document_count', string='# Documents')


class OpStudentAttachment(models.Model):
    _inherit = 'ir.attachment'

    doc_attach_rel = fields.Many2many('hr.document', 'doc_attachment_id', 'attach_id3', 'doc_id',
                                      string="Attachment", invisible=1)