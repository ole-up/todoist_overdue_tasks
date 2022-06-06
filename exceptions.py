class ApiServiceError(Exception):
    """Program can't receive task"""


class FormattingError(Exception):
    """Program can't format tasks list"""


class SaverError(Exception):
    """Program can't save tasks report"""


class EmailError(Exception):
    """Program can't send email"""
