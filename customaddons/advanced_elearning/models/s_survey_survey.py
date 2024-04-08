from odoo import models, api, fields, _
from odoo.exceptions import UserError
import random

class SSurveySurvey(models.Model):
    _inherit = "survey.survey"

    assignment = fields.Many2many('res.users', 'assignment_survey', string='Assignment')
    total_score = fields.Float("Total Score")
    group_1_random = fields.Integer("", default=0)
    group_2_random = fields.Integer("", default=0)
    group_3_random = fields.Integer("", default=0)
    group_4_random = fields.Integer("", default=0)
    group_1_count = fields.Integer('Questions', compute='compute_count_group_questions')
    group_2_count = fields.Integer('Questions', compute='compute_count_group_questions')
    group_3_count = fields.Integer('Questions', compute='compute_count_group_questions')
    group_4_count = fields.Integer('Questions', compute='compute_count_group_questions')

    def _prepare_user_input_predefined_questions(self):
        self.ensure_one()
        if self.questions_selection == 'all':
            return self.question_ids
        else:
            group_1_random = self.group_1_random
            group_2_random = self.group_2_random
            group_3_random = self.group_3_random
            group_4_random = self.group_4_random
            questions = self.env['survey.question']

            group_1_questions = self.question_ids.filtered(lambda q: q.question_group == '1')
            group_2_questions = self.question_ids.filtered(lambda q: q.question_group == '2')
            group_3_questions = self.question_ids.filtered(lambda q: q.question_group == '3')
            group_4_questions = self.question_ids.filtered(lambda q: q.question_group == '4')
            no_group_questions = self.question_ids.filtered(lambda q: q.question_group == False)
            questions |= no_group_questions

            if group_1_random > len(group_1_questions):
                questions |= group_1_questions
            else:
                questions_1 = questions.concat(*random.sample(group_1_questions, group_1_random))
                questions |= questions_1
            if group_2_random > len(group_2_questions):
                questions |= group_2_questions
            else:
                questions_2 = questions.concat(*random.sample(group_2_questions, group_2_random))
                questions |= questions_2
            if group_3_random > len(group_3_questions):
                questions |= group_3_questions
            else:
                questions_3 = questions.concat(*random.sample(group_3_questions, group_3_random))
                questions |= questions_3
            if group_4_random > len(group_4_questions):
                questions |= group_4_questions
            else:
                questions_4 = questions.concat(*random.sample(group_4_questions, group_4_random))
                questions |= questions_4
            return questions

    def compute_count_group_questions(self):
        for rec in self:
            rec.group_1_count = 0
            rec.group_2_count = 0
            rec.group_3_count = 0
            rec.group_4_count = 0
            if rec.question_ids:
                rec.group_1_count = len(rec.question_ids.filtered(lambda q: q.question_group == '1'))
                rec.group_2_count = len(rec.question_ids.filtered(lambda q: q.question_group == '2'))
                rec.group_3_count = len(rec.question_ids.filtered(lambda q: q.question_group == '3'))
                rec.group_4_count = len(rec.question_ids.filtered(lambda q: q.question_group == '4'))
