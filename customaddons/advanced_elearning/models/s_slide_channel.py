from odoo import models, fields, api
from odoo.exceptions import UserError

class SSlideChannel(models.Model):
    _inherit = "slide.channel"


    assignment = fields.Many2many('res.users','assignment_channel', string='Assignment')

    # Update noupdate in ir_model_data -> update record rules
    def init(self):
        self.env.cr.execute("""UPDATE ir_model_data SET noupdate = 'false' WHERE model = 'ir.rule'""")
