from pydantic import BaseModel, Field


class Document(BaseModel):
    """Extract key information from this document."""

    title: str = Field(description="The document title")
    summary: str = Field(description="A brief summary in 1-2 sentences")
    key_points: list[str] = Field(description="3-5 main points")


chat = chatlas.ChatOllama(model="gemma3")
result = chat.chat_structured(
    "https://e-lib.iclei.org/publications/data-projects-in-monterrey-mexico.pdf",
    data_model=Document,
)

print(result.title)
print(result.summary)
for point in result.key_points:
    print(f"- {point}")
