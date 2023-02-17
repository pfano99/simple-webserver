def extract_path_from_request(request: str):
    path = request[request.find(" "):request.find("HTTP")]
    return path

