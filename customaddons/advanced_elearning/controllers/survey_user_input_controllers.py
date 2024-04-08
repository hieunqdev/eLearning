from odoo.addons.survey.controllers.main import Survey
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class SurveyUploadFile(Survey):
    @http.route('/survey/submit/<string:survey_token>/<string:answer_token>', type='json', auth='public', website=True)
    def survey_submit(self, survey_token, answer_token, **post):
        res = super(SurveyUploadFile, self).survey_submit(survey_token, answer_token, **post)

        survey_id_results = request.env['survey.survey'].sudo().search([('access_token', '=', survey_token)])
        question_id_results = request.env['survey.question'].sudo().search(
            [('survey_id', '=', survey_id_results.id), ('question_type', '=', 'upload_file')])
        if question_id_results:
            user_input_id_results = request.env['survey.user_input.line'].search([], order='user_input_id asc', limit=1)
            question_id = question_id_results.mapped('id')
            name_file = 0
            for id in question_id:
                request.env['survey.user_input.line'].sudo().create({
                    'user_input_id': user_input_id_results.user_input_id.id,
                    'survey_id': survey_id_results.id,
                    'question_id': id,
                    'skipped': False,
                    'answer_type': 'upload_file',
                    'value_upload_file': post.get(str(name_file) + 'base64'),
                    'file_name': post.get(str(name_file))
                })
                name_file += 1
            request.env['survey.user_input.line'].sudo().search(
                [('skipped', '=', True), ('question_id', 'in', question_id)]).unlink()

        return res
