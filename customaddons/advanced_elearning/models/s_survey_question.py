from odoo import models, api, fields
from odoo.exceptions import ValidationError


class SSurveyQuestion(models.Model):
    _inherit = "survey.question"

    question_group = fields.Selection([("1", "Group 1"), ("2", "Group 2"), ("3", "Group 3"), ("4", "Group 4")],
                                      string="Group", default="1")
    title = fields.Html(string='Title')
    total_score_of_the_sentence = fields.Float(string="Total Score Of The Sentence", required=True)
    value_binary = fields.Binary(string='Value Binary', attachment=True)
    question_type = fields.Selection(selection_add=[
        ('upload_file', 'Upload File')
    ])

    @api.constrains('total_score_of_the_sentence')
    def _check_total_score_of_the_sentence(self):
        for r in self:
            if r.total_score_of_the_sentence < 0:
                raise ValidationError('giá trị tổng điểm của câu phải lớn hơn 0')

    @api.onchange('total_score_of_the_sentence')
    def _onchange_total_score_of_the_sentence(self):
        count = self.suggested_answer_ids.search_count([('question_id', 'in', self.ids), ('is_correct', '=', True)])
        answers = self.suggested_answer_ids.search([('question_id', 'in', self.ids)])
        for answer in answers:
            if self.total_score_of_the_sentence and answer.is_correct:
                answer.answer_score = self.total_score_of_the_sentence / count
            else:
                answer.answer_score = 0
