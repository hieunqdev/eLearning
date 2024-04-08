odoo.define('advanced_elearning.form', function (require) {
    'use strict';

    var Form = require('survey.form');
    Form.include({
        _prepareSubmitValues: function (formData, params) {
            var self = this;
            formData.forEach(function (value, key) {
                switch (key) {
                    case 'csrf_token':
                    case 'token':
                    case 'page_id':
                    case 'question_id':
                        params[key] = value;
                        break;
                }
            });

            // Get all question answers by question type
            this.$('[data-question-type]').each(function () {
                switch ($(this).data('questionType')) {
                    case 'text_box':
                    case 'upload_file':
                    case 'char_box':
                    case 'numerical_box':
                        params[this.name] = this.value;
                        break;
                    case 'date':
                        params = self._prepareSubmitDates(params, this.name, this.value, false);
                        break;
                    case 'datetime':
                        params = self._prepareSubmitDates(params, this.name, this.value, true);
                        break;
                    case 'simple_choice_radio':
                    case 'multiple_choice':
                        params = self._prepareSubmitChoices(params, $(this), $(this).data('name'));
                        break;
                    case 'matrix':
                        params = self._prepareSubmitAnswersMatrix(params, $(this));
                        break;
                }
            });
        },
    });
});