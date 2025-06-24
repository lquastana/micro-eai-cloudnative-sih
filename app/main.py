from multiprocessing import Process
import uvicorn
from loguru import logger

from .api.main import app
from .mllp.server import serve


if __name__ == "__main__":
    logger.info("Starting MLLP server and API")
    mllp_process = Process(target=serve)
    mllp_process.start()
    uvicorn.run(app, host="0.0.0.0", port=8000)
    mllp_process.join()
