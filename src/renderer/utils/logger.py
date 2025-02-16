# src/renderer/utils/logger.py
import logging

def setup_logger():
    logging.basicConfig(
        level=logging.DEBUG, # Change to INFO or WARNING as needed
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    return logging.getLogger("PyBlenderRender")

logger = setup_logger()
