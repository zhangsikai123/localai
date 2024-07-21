from configs import API_SERVER


def run_api_server():
    import uvicorn

    host = API_SERVER["host"]
    port = API_SERVER["port"]
    uvicorn.run("server.api:create_app", host=host, port=port, reload=True)


if __name__ == "__main__":
    run_api_server()
