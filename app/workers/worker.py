"""arq background worker settings and task routing."""
import logging
from arq.connections import RedisSettings
from app.config import settings

logger = logging.getLogger("chai_sutta.worker")


async def startup(ctx: dict) -> None:
    """Worker startup hook."""
    logger.info("Starting Chai Sutta background worker...")
    ctx["some_state"] = "initialized"


async def shutdown(ctx: dict) -> None:
    """Worker shutdown hook."""
    logger.info("Stopping Chai Sutta background worker...")


async def dummy_task(ctx: dict) -> str:
    """A placeholder task to ensure worker has at least one registered function."""
    logger.info("Executing dummy setup task...")
    return "done"


# arq worker configuration class
class WorkerSettings:
    """Worker settings class for arq."""
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)
    functions = [dummy_task]  # Must have at least one task
    on_startup = startup
    on_shutdown = shutdown
    max_jobs = 10
    job_timeout = 600  # 10 minutes timeout for heavy tasks
