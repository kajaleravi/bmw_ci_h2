from message_handler import MessageHandler
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProductionStats:
    sent: int
    received: int
    priority_avg: float

class CommunicationChannel:
    """BMW production channel with CI-CD integration"""
    
    def __init__(self, channel_name: str):
        self.channel_name = channel_name
        self.handler = MessageHandler()
        self.stats: Dict[str, ProductionStats] = {}
        logger.info(f"BMW production channel initialized: {self.channel_name}")

    def process_message(self, sender: str, recipient: str, content: str) -> Tuple[bool, str]:
        """Process BMW production messages with validation"""
        success, message = self.handler.send_message(sender, recipient, content)
        if not success:
            logger.error(f"Message processing failed: {message}")
            return (False, message)
        
        if sender not in self.stats:
            self.stats[sender] = ProductionStats(0, 0, 0.0)
        self.stats[sender].sent += 1
        
        if recipient not in self.stats:
            self.stats[recipient] = ProductionStats(0, 0, 0.0)
        self.stats[recipient].received += 1
        
        logger.info(f"Processed BMW message on {self.channel_name}: {content}")
        return (success, f"{message} via {self.channel_name}")

    def get_production_stats(self) -> Dict[str, Tuple[int, int, float]]:
        """Return BMW production statistics"""
        stats = {
            unit: (stats.sent, stats.received, stats.priority_avg)
            for unit, stats in self.stats.items()
        }
        logger.debug(f"BMW production stats: {stats}")
        return stats

    def analyze_production(self, unit: str) -> Optional[List[Tuple[str, str, float]]]:
        """Analyze BMW production unit messages"""
        messages = self.handler.get_production_messages(unit)
        if not messages:
            logger.warning(f"No messages found for BMW unit {unit}")
            return None
        
        total_priority = sum(self.handler._calculate_priority(content) 
                           for _, content, _ in messages)
        avg_priority = total_priority / len(messages) if messages else 0
        self.stats[unit].priority_avg = avg_priority
        logger.info(f"Analyzed {unit}: {len(messages)} messages, avg priority {avg_priority}")
        return messages