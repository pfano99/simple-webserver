import pathlib

FILE_TYPES = {
    "text": "text/plain",
    "css": "text/css",
    "html": "text/html",
    "csv": "text/csv",
    "png": "image/png",
    "json": "application/json",
    "js": "application/javascript"
}


class ResourceReader:

    def __init__(self) -> None:
        self._resp = {
            "status": 0,
            "body": b"",
            "size": 0,
            "resource_type": "text/plain"
        }

    @staticmethod
    def _determine_resource_type(resource_path):
        ext = pathlib.Path(resource_path).suffix
        ext = ext.replace(".", "")
        _type = FILE_TYPES.get(ext)
        return _type if _type else "text/plain"

    def read_resource_file(self, filename: str) -> dict:
        try:
            with open(filename, "rb") as file:
                data = file.read()
            self._resp["body"] = data
            self._resp["size"] = len(self._resp["body"])
            self._resp["status"] = 200
            self._resp["resource_type"] = self._determine_resource_type(filename)
            return self._resp

        except FileNotFoundError as e:
            print(e)
            self._resp["status"] = 404
            return self._resp

        except UnicodeDecodeError as e:
            print(e)
            self._resp["status"] = 400
            return self._resp

        except Exception as e:
            print(e)
            self._resp["status"] = 500
            return self._resp
