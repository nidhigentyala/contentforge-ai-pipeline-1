from config import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def research_topic(topic: str) -> dict:
    """
    Research a given topic and return structured research data.

    Returns:
        {
            "topic": str,
            "research_summary": str,
            "key_points": list[str],
            "sources": list[str]
        }
    """

    prompt = ChatPromptTemplate.from_template(
        """You are a research assistant. Research the topic below and return ONLY valid JSON, nothing else.

Topic: {topic}

Return JSON with exactly these keys:
- research_summary: a 150-200 word summary of the topic
- key_points: a list of exactly 5 short factual bullet points
- sources: a list of 3 plausible reference/source names related to this topic
"""
    )

    chain = prompt | llm | JsonOutputParser()

    result = chain.invoke({"topic": topic})

    result["topic"] = topic

    return result