from config import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

def edit_content(draft: dict) -> dict:
    """
    Input:  the exact dict write_draft() returns
    Output: {"final_content": str, "edits_made": list[str], "tone_check": str}
    """
    prompt = ChatPromptTemplate.from_template(
        """You are a professional editor. Improve the article below for clarity, grammar, and flow.
        
        CRITICAL INSTRUCTION: You must return ONLY a raw, valid JSON object. 
        - Do NOT include markdown formatting (like ```json)
        - Do NOT include any conversational text before or after the JSON
        - Escape any internal quotation marks properly

        Article: {draft_content}

        Return JSON with exactly these keys:
        - "final_content": the fully edited, polished article text
        - "edits_made": a list of 3-5 short strings describing what you improved
        - "tone_check": one word describing the final tone (e.g. "professional", "casual", "technical")
        """
    )
    chain = prompt | llm | JsonOutputParser()
    result = chain.invoke({"draft_content": draft["draft_content"]})
    return result