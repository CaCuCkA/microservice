import consul
import logging
from abc import ABC
from flask import jsonify
from typing import List, Generator


class BaseService(ABC):
    def __init__(self, app, service_id: str, port: int) -> None:
        super().__init__()
        self._app = app
        self._consul_client: consul.Consul = BaseService.__service_register(service_id, port) 
        

    @staticmethod
    def __service_register(service_id: str, port: int) -> consul.Consul:
        service_name = service_id.rsplit('_', 1)[0]
        client = consul.Consul(host='consul')
        check = consul.Check.http(f"http://{service_id}:{port}/health", interval="10s")
        client.agent.service.register(name=service_name,
                             service_id=service_id,
                             address=f"http://{service_id}:{port}",
                             port=port,
                             check=check)
        return client

    @staticmethod
    def _camel_to_snake(name: str, id: int = None):
        import re
        snake_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        snake_name = re.sub('([a-z0-9])([A-Z])', r'\1_\2', snake_name).lower()
        return snake_name if id is None else f"{snake_name}_{id}"
    
    @staticmethod
    def setup_logging():
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
