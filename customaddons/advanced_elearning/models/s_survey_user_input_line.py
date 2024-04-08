from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero


class SSurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    answer_type = fields.Selection(selection_add=[
        ('upload_file', 'Upload File')
    ])
    value_upload_file = fields.Binary(string='Value Upload File', readonly=True, attachment=True)
    file_name = fields.Char(string='file name')
