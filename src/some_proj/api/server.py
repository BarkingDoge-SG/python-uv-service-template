import logging
from fastapi import FastAPI
from pydantic import BaseModel
from contextlib import asynccontextmanager

from common_utils.logger import Logger
from src.some_proj.some_file import(
    some_func
)

LOGGER = Logger("some_proj_api").get_logger()
logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class RequestItem(BaseModel):
    something: str


class ResponseItem(BaseModel):
    something: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    LOGGER.info("==== Starting Harm Classifier API ====")

    try:
        something = some_func()
        app.state.something = something
        app.state.ready = True

        LOGGER.info("something is loaded and API is READY.")

    except Exception as e:
        LOGGER.exception(f"Failed during startup: {e}")
        raise e

    try:
        yield

    finally:
        LOGGER.info("Shutting down API...")

        something = getattr(app.state, "something", None)
        if something is not None:
            LOGGER.info("Releasing model from memory...")
            del app.state.model

        app.state.ready = False

        # if DEVICE == "cuda":
        #     LOGGER.info("Clearing CUDA cache...")
        #     torch.cuda.empty_cache()

        LOGGER.info("API shutdown complete.")


app = FastAPI(title="Something API", lifespan=lifespan)


@app.post("/some_call")
async def some_function(request: RequestItem):
    something = request.something

    ...

    return ResponseItem(
        something=...
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("some_proj.api.server:app", host="0.0.0.0", port=8080, reload=False)
