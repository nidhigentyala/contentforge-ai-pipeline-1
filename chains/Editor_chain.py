from config import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def edit_content(draft: dict) -> dict:
    """
    Input:
        The exact dictionary returned by write_draft()
        {
            "draft_content": str,
            "word_count": int
        }

    Output:
        {
            "final_content": str,      # polished final article
            "edits_made": list[str],   # short list of what was fixed
            "tone_check": str          # e.g. "professional", "casual"
        }
    """

    prompt = ChatPromptTemplate.from_template(
        """You are a professional editor.
Improve the article below for clarity, grammar, and flow.
Return ONLY valid JSON, nothing else.

Article: {draft_content}

Return JSON with exactly these keys:
- final_content: the fully edited, polished article text
- edits_made: a list of 3-5 short strings describing what you improved
- tone_check: one word describing the final tone (e.g. "professional", "casual", "technical")

Do not add any other keys."""
    )

    chain = prompt | llm | JsonOutputParser()

    result = chain.invoke({"draft_content": draft["draft_content"]})

    return result