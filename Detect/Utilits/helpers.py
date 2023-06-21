import datetime
import logging
import html.entities


class Helpers:

    @staticmethod
    def date_validate(date_text: str) -> bool:
        """
        Вспомогательная функция контроллера для валидации даты
            date_text: строка даты в формате 2023-12-25 (YYYY-MM-DD)

            :return bool
        """
        try:
            datetime.date.fromisoformat(date_text)
            return True
        except Exception as e:
            logging.exception(e)
            return False

    @staticmethod
    def escape(text: str) -> str:
        if text is None:
            return ''

        return html.entities.codepoint2name[ord(text)]

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'csv', 'docx'])
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS