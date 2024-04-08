odoo.define('advanced_elearning.survey_page_fill_inherit', function (require) {
    "use strict";

    $(function () {
        $('a').each(function () {
            $(this).hover(function () {
                $(this).addClass("over");
            }, function () {
                $(this).removeClass("over");
            });
        });

        $(document).on("click", ".menu-text", function () {
            let text = $(this).attr("id");
            const element = document.getElementById(text);
            element.scrollIntoView();
        });
    });
});






