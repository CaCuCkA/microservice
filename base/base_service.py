import logging
from abc import ABC
from flask import jsonify
from typing import List, Generator


class BaseService(ABC):
    def __init__(self, app) -> None:
        super().__init__()
        self._app = app
        self.__setup_logging()

    def __setup_logging(self):
        """Setup logging for project"""
        logging.basicConfig(
            filename="logs.txt",
            format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
            filemode="a+",
            level=logging.INFO)

    def _message_parser(self, data, args: List[str]) -> Generator:
        """Parse specified arguments from a data dictionary."""
        return (data.get(arg) for arg in args)

    def _logger(self, message: str):
        """Log a message to the console."""
        self._app.logger.info(message)

    def _generate_output(self, **kwargs):
        """Generate a successful JSON response."""
        return jsonify({"status": "success", **kwargs}), 200
    
    def handle_error(self, error_msg: str):
        """Generate an error JSON response."""
        return jsonify({"error": error_msg}), 500
