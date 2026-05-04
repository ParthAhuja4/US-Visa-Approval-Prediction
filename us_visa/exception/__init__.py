import types


def error_message_detail(error: str | Exception, error_detail: types.ModuleType) -> str:
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is None:
        return f"Error occurred: {str(error)} (no traceback available)"

    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )

    return error_message


class USvisaException(Exception):
    def __init__(
        self, error_message: Exception, error_detail: types.ModuleType
    ) -> None:
        """
        :param error_message: error message in string format
        :param error_detail: the sys module, used to extract traceback info
        """
        super().__init__(error_message)
        self.error_message = error_message_detail(
            error_message, error_detail=error_detail
        )

    def __str__(self) -> str:
        return self.error_message
