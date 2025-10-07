import uvicorn

if __name__ == "__main__":
    # For local dev, binding to all interfaces is OK.
    # For CI, suppress Bandit warning.
    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",  # nosec
        port=8000,
        reload=True
    )