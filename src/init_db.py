import logging

from database.engine import engine
from database.models import Base

logger = logging.getLogger(__name__)

logger.info("Initializing models")
Base.metadata.create_all(engine)
