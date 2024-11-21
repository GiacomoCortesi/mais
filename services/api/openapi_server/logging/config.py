# logging/config.py
import logging
import logging.config
import json
from pathlib import Path
from typing import Dict, Any
from datetime import datetime

def setup_logging(
    config_path: Path = Path("openapi_server/logging/config.json"),
) -> None:
    with open(config_path, 'r') as f:
        config = json.load(f)
    logging.config.dictConfig(config)

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_dict: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        if record.exc_info:
            log_dict["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra_fields"):
            log_dict.update(record.extra_fields)
            
        return json.dumps(log_dict)