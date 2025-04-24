from typing import Tuple, Dict, List, Optional
from collections import defaultdict
import json
from datetime import datetime
import os
import logging
import logging.config  # Explicitly import logging.config
import yaml

with open("logging_config.yaml", 'r') as f:
    logging.config.dictConfig(yaml.safe_load(f))
logger = logging.getLogger(__name__)

class MessageHandler:
    """Manages BMW production messages with CI-CD safeguards"""
    
    def __init__(self, storage_path: str = "bmw_production.json"):
        self.storage_path = storage_path
        self.message_store: Dict[Tuple[str, float], List[Tuple[str, str, int]]] = defaultdict(list)
        self._load_from_file()
        logger.info("Initialized BMW MessageHandler for production tracking")

    def send_message(self, sender: str, recipient: str, content: str) -> Tuple[bool, str]:
        """Send BMW production updates with validation"""
        if not all([sender, recipient, content]):
            logger.error("Invalid message parameters")
            return (False, "Message parameters cannot be empty")
        
        timestamp = datetime.now().timestamp()
        priority = self._calculate_priority(content)
        message_tuple = (recipient, content, priority)
        
        self.message_store[(sender, timestamp)].append(message_tuple)
        self._save_to_file()
        
        logger.info(f"BMW production message from {sender} to {recipient}: {content}")
        return (True, f"BMW update logged at {timestamp}")

    def get_production_messages(self, recipient: str) -> List[Tuple[str, str, float]]:
        """Retrieve BMW production messages"""
        result = []
        for (sender, timestamp), messages in self.message_store.items():
            for msg_recipient, content, priority in messages:
                if msg_recipient == recipient:
                    result.append((sender, content, timestamp))
        
        logger.debug(f"Retrieved {len(result)} messages for {recipient}")
        return sorted(result, key=lambda x: x[2], reverse=True)

    def _calculate_priority(self, content: str) -> int:
        """Calculate priority based on BMW production keywords"""
        keywords = {
            "m5_engine_failure": 5,
            "x5_assembly_delay": 3,
            "i4_production": 2,
            "bmw_routine_check": 1
        }
        content_lower = content.lower()
        priority = max((keywords.get(word, 0) for word in content_lower.split()), default=0)
        logger.debug(f"Priority {priority} for: {content}")
        return priority

    def _save_to_file(self) -> None:
        """Persist BMW production data with error handling"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump({
                    "messages": {
                        f"{sender}_{ts}": [list(msg) for msg in messages]
                        for (sender, ts), messages in self.message_store.items()
                    }
                }, f, indent=2)
            logger.info("Production data saved successfully")
        except Exception as e:
            logger.error(f"Failed to save production data: {str(e)}")
            raise

    def _load_from_file(self) -> None:
        """Load BMW production history"""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    for key, messages in data["messages"].items():
                        sender, ts = key.rsplit("_", 1)
                        self.message_store[(sender, float(ts))] = [
                            tuple(msg) for msg in messages
                        ]
                logger.info("Loaded BMW production history")
            except Exception as e:
                logger.error(f"Failed to load production data: {str(e)}")
                raise