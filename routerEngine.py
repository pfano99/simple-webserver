import os

from pathlib import Path
from datetime import datetime

STATUS_CODES = {
    200: "OK",
    204: "No Content",
    400: "Bad Request",
    404: "NOT FOUND",
    411: "Length Required",
    415: "Unsupported Media Type",
    500: "Internal Server Error",
    501: "Not Implemented",
    505: "HTTP Version Not Supported"
}


def file_exits_in_path(path):
    return os.path.exists(path)


def generate_http_response(status_code: int, headers: dict, response_body: str) -> bytes:
    assert status_code in STATUS_CODES.keys()
    return """
                HTTP/1.1 {} {}\r\n
                Date: {}\r\n
                Server: {}\r\n\r\n
            """.format(
        status_code,
        STATUS_CODES[status_code],
        datetime.utcnow(),
        "Simple server"
    ).encode("utf-8")


class REngine(object):

    def __init__(self, templates_folder_name="templates", default_starter_page_name="index.html"):
        self.templates_folder_name = templates_folder_name
        self.default_starter_page_name = default_starter_page_name

    def process_path(self, file_path: str):
        """
        Only match endpoint should have the same name as the file
        example: /home should have a file home.html
        :param file_path: path requested by the client, e.g /home
        :return:
        """
        current_path = Path.cwd()

        requested_path = file_path.strip()
        if not len(requested_path) > 1:
            return os.path.join(current_path, self.templates_folder_name, self.default_starter_page_name)
        else:
            return os.path.join(current_path, self.templates_folder_name, *requested_path.split("/"))


if __name__ == '__main__':
    print(REngine().process_path("/index.html"))
