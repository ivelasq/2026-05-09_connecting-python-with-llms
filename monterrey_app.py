import chatlas
import os
from shiny.express import ui

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


# Page title
ui.page_opts(title="PyLadies Monterrey Event Assistant")

# Add header
ui.markdown("""
Ask me about:
- Upcoming events (e.g., "What events do we have about AI?")
- Venue information (e.g., "Tell me about TEC de Monterrey")
- Attendance statistics (e.g., "What's our average attendance?")
""")

# Create chat interface
chat = ui.Chat(
    id="chat",
    messages=[
        {
            "role": "assistant",
            "content": "¡Hola! I'm your PyLadies Monterrey assistant. Ask me about our events, venues, or attendance stats!",
        }
    ],
)
chat.ui()

# Create chatbot with tools
chat_model = chatlas.ChatAnthropic(
    model="claude-sonnet-4-5",
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    system_prompt="""You are a helpful assistant for PyLadies Monterrey.
    You can help members find information about events, venues, and attendance statistics.
    Always be friendly and encouraging about Python learning!

    IMPORTANT: Respond bilingually in both English and Spanish. Use this format:
    - Start with a Spanish greeting or main point
    - Follow with the English translation or explanation
    - Mix both languages naturally throughout your response
    - Example: "¡Claro! / Of course! Tenemos varios eventos / We have several events..."
    """,
)

# Register the tools
chat_model.register_tool(get_upcoming_events)
chat_model.register_tool(get_venue_info)
chat_model.register_tool(calculate_attendance_stats)


@chat.on_user_submit
async def handle_user_input():
    """Handle user messages and stream responses"""
    user_message = chat.user_input()
    response = chat_model.stream(user_message)
    await chat.append_message_stream(response)
