from communication_channel import CommunicationChannel
import logging

logger = logging.getLogger(__name__)

def main():
    channel = CommunicationChannel("BMW_Munich_Plant")
    logger.info("Starting BMW production monitoring")

    # BMW production examples
    channel.process_message("Engine_Team", "Assembly_Line", "M5_engine_failure detected in production")
    channel.process_message("Assembly_Line", "Quality_Control", "X5_assembly_delay due to parts shortage")
    channel.process_message("Maintenance", "Engine_Team", "BMW_routine_check for i4 production completed")

    # Analyze production
    engine_messages = channel.analyze_production("Engine_Team")
    if engine_messages:
        print("Engine Team BMW Updates:")
        for sender, content, ts in engine_messages:
            print(f"[{ts}] From {sender}: {content}")

    # Production stats
    stats = channel.get_production_stats()
    print("\nBMW Production Statistics:")
    for unit, (sent, received, avg_priority) in stats.items():
        print(f"{unit}: Sent={sent}, Received={received}, Avg Priority={avg_priority:.2f}")

if __name__ == "__main__":
    main()