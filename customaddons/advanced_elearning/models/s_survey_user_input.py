from odoo import models, fields, api, _


class SServeyUserInput(models.Model):
    _inherit = "survey.user_input"
    # compute_sudo dùng để thực hiện tính toán lại với quyền supperuser
    scoring_percentage = fields.Float("Score (%)", compute="_compute_scoring_values", store=True,
                                      compute_sudo=True)  # stored for perf reasons
    scoring_total = fields.Float("Total Score", compute="_compute_scoring_values", store=True,
                                 compute_sudo=True)  # stored for perf reasons

    @api.depends('user_input_line_ids.answer_score', 'user_input_line_ids.question_id',
                 'predefined_question_ids.answer_score')
    def _compute_scoring_values(self):
        for user_input in self:
            # sum(multi-choice question scores) + sum(simple answer_type scores)
            total_possible_score = 0
            for question in user_input.predefined_question_ids:
                count_answer_true = self.env['survey.question.answer'].search_count(
                    [('question_id', '=', question.id), ('is_correct', '=', True)])
                result_simple_choice = user_input.user_input_line_ids.search(
                    [('question_id', '=', question.id), ('id', 'in', user_input.user_input_line_ids.ids)])
                result_multiple_answers = user_input.user_input_line_ids.search(
                    [('question_id', '=', question.id), ('id', 'in', user_input.user_input_line_ids.ids)])
                if question.question_type == 'simple_choice':
                    if result_simple_choice.mapped('answer_is_correct'):
                        total_possible_score += max(
                            [score for score in result_simple_choice.mapped('answer_score') if score > 0], default=0)
                elif question.question_type == 'multiple_choice':
                    if len(result_multiple_answers.mapped('answer_is_correct')) >= count_answer_true:
                        if all([select == True for select in result_multiple_answers.mapped('answer_is_correct')]):
                            total_possible_score += sum(
                                score for score in result_multiple_answers.mapped('answer_score') if score > 0)

                elif question.is_scored_question:
                    total_possible_score += question.answer_score

            if total_possible_score == 0:
                user_input.scoring_percentage = 0
                user_input.scoring_total = 0
            else:
                sentence_point = self.env['survey.question.answer'].search(
                    [('question_id', 'in', user_input.predefined_question_ids.ids)]).mapped('answer_score')
                score_total = sum(score for score in sentence_point if score > 0)
                user_input.scoring_total = score_total
                score_percentage = (total_possible_score / score_total) * 100
                user_input.scoring_percentage = round(score_percentage, 2) if score_percentage > 0 else 0

    def mark(self):
        if self.access_token:
            answer_token = self.access_token
            survey_survey = self.env['survey.survey'].search([('id', '=', self.survey_id.id)])
            question_token = survey_survey.access_token

            return {
                'type': 'ir.actions.act_url',
                'url': '/survey/print/%s?answer_token=%s&amp;review=True' % (question_token, answer_token),
                'target': 'new',
            }

    def save_lines(self, question, answer, comment=None):
        old_answers = self.env['survey.user_input.line'].search([
            ('user_input_id', '=', self.id),
            ('question_id', '=', question.id)
        ])

        if question.question_type in ['char_box', 'text_box', 'numerical_box', 'date', 'datetime', 'upload_file']:
            self._save_line_simple_answer(question, old_answers, answer)
            if question.save_as_email and answer:
                self.write({'email': answer})
            if question.save_as_nickname and answer:
                self.write({'nickname': answer})

        elif question.question_type in ['simple_choice', 'multiple_choice']:
            self._save_line_choice(question, old_answers, answer, comment)
        elif question.question_type == 'matrix':
            self._save_line_matrix(question, old_answers, answer, comment)

        elif question.question_type == 'upload_file':
            self._save_line_simple_answer(question, old_answers, answer)
        else:
            raise AttributeError(question.question_type + ": This type of question has no saving function")
