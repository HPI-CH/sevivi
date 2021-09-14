"""Sets up the logging format"""
import logging

FORMAT = "[%(lineno)3s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)
logger = logging.getLogger("sevivi")
logger.setLevel(logging.DEBUG)
