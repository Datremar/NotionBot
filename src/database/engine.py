import logging

from sqlalchemy import create_engine


logger = logging.getLogger(__name__)

logger.info("Initializing engine")
engine = create_engine('sqlite:///src/database/database.db')
