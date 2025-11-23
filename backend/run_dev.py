import uvicorn


def main() -> None:
    """Starting FastAPI-application in development mode with Uvicorn."""
    uvicorn.run(
        "src.main:app",
        workers=1,
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


if __name__ == "__main__":
    main()
