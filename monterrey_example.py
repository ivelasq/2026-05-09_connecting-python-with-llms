"""
Monterrey PyLadies Event Assistant
A chatbot that can access local event data and venue information
"""

import chatlas

# Simulated local database of PyLadies Monterrey events
EVENTS = [
    {
        "name": "Python & LLMs Workshop",
        "date": "2026-05-09",
        "location": "TEC de Monterrey",
        "attendees": 45,
        "topic": "chatlas and AI",
    },
    {
        "name": "Data Science Night",
        "date": "2026-04-15",
        "location": "Café Punto Medio",
        "attendees": 30,
        "topic": "pandas and visualization",
    },
    {
        "name": "Web Development Workshop",
        "date": "2026-03-20",
        "location": "Co-working Monterrey",
        "attendees": 25,
        "topic": "Flask and Django",
    },
]

# Simulated venue data
VENUES = {
    "TEC de Monterrey": {
        "capacity": 100,
        "wifi": True,
        "projector": True,
        "address": "Av. Eugenio Garza Sada 2501",
    },
    "Café Punto Medio": {
        "capacity": 40,
        "wifi": True,
        "projector": False,
        "address": "Padre Mier 1133 Pte",
    },
    "Co-working Monterrey": {
        "capacity": 50,
        "wifi": True,
        "projector": True,
        "address": "Blvd. Antonio L. Rodríguez 1888",
    },
}


def get_upcoming_events(topic: str = None):
    """
    Get upcoming PyLadies Monterrey events.

    Parameters
    ----------
    topic : str, optional
        Filter by topic (e.g., "AI", "data", "web")
    """
    events = EVENTS.copy()

    if topic:
        events = [e for e in events if topic.lower() in e["topic"].lower()]

    return events


def get_venue_info(venue_name: str):
    """
    Get information about a venue in Monterrey.

    Parameters
    ----------
    venue_name : str
        Name of the venue
    """
    venue = VENUES.get(venue_name)
    if not venue:
        return f"Venue '{venue_name}' not found in database"
    return venue


def calculate_attendance_stats():
    """Calculate total and average attendance for all PyLadies Monterrey events."""
    total = sum(e["attendees"] for e in EVENTS)
    avg = total / len(EVENTS)
    return {
        "total_attendees": total,
        "average_per_event": round(avg, 1),
        "total_events": len(EVENTS),
    }


# Create the chatbot and register tools
# Set ANTHROPIC_API_KEY environment variable before running
chat = chatlas.ChatAnthropic(
    model="claude-sonnet-4-5",
    system_prompt="""You are a helpful assistant for PyLadies Monterrey.
    You can help members find information about events, venues, and attendance statistics.
    Always be friendly and encouraging about Python learning!""",
)

chat.register_tool(get_upcoming_events)
chat.register_tool(get_venue_info)
chat.register_tool(calculate_attendance_stats)


if __name__ == "__main__":
    print("🐍 PyLadies Monterrey Event Assistant")
    print("=" * 50)
    print("\nExample questions you can ask:")
    print("- What events do we have about AI?")
    print("- Tell me about the TEC de Monterrey venue")
    print("- What's our average event attendance?")
    print("- Where is our next data science event?")
    print("\n" + "=" * 50 + "\n")

    # Example interactions
    examples = [
        "What events do we have about AI or data?",
        "Tell me about the TEC de Monterrey venue - does it have a projector?",
        "What's our total attendance across all events?",
    ]

    for question in examples:
        print(f"\n👤 Question: {question}")
        print("🤖 Response: ", end="")
        response = chat.chat(question)
        print()
