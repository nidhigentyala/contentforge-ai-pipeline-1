from config import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


def write_draft(outline: dict) -> dict:
    """
    Input:
        The exact dictionary returned by create_outline()

    Output:
        {
            "draft_content": str,
            "word_count": int
        }
    """

    prompt = ChatPromptTemplate.from_template(
        """You are a professional content writer.

Write a complete, well-structured article based on the outline below.

Title:
{title}

Sections:
{sections}

Instructions:
- Write a complete article covering every section.
- Use clear and natural language.
- Make the article flow logically from one section to the next.
- Expand the key points into useful paragraphs.
- Do not invent unrelated information.
- Do not return JSON.
- Return only the article text.
"""
    )

    chain = prompt | llm | StrOutputParser()

    draft_text = chain.invoke(
        {
            "title": outline["title"],
            "sections": outline["sections"],
        }
    )

    return {
        "draft_content": draft_text,
        "word_count": len(draft_text.split()),
    }