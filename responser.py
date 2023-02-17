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


class HttpResponseBuilder:

    def __init__(self, http_version: str = "HTTP/1.1"):
        self._http_version: str = http_version
        self._response: str = str()

    def _add_status_line(self, status_code: int, ) -> None:
        assert status_code in STATUS_CODES.keys()
        self._response += "{} {} {}\r\n".format(self._http_version, status_code, STATUS_CODES[status_code])

    def _add_header_fields(self, headers: dict) -> None:
        assert headers is not None
        for header in headers.keys():
            print("headers = ", header)
            self._response += " {}: {}\r\n".format(header, headers[header])

    def _add_body(self, body: str) -> None:
        body = body if body is not None else "".encode("utf-8")
        self._response += "\r\n"
        self._response = self._response.encode("utf-8")
        self._response += body

    def build(self, status_code: int, headers: dict, body: str) -> str:
        self._add_status_line(status_code)
        self._add_header_fields(headers)
        self._add_body(body)
        return self._response
