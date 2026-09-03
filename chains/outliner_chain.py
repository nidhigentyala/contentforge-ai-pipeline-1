from config import llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser


def create_outline(research_data: dict) -> dict:
    """
    Input: 
        The exact dictionary returned by the research_topic()
    Output:
        {
            "title": str,
            "sections": [
                {
                    heading: str,
                    "key_points": list[str]
                }
            ]
        }
    """
    prompt = ChatPromptTemplate.from_template(
        """You are acontent outliner.
    use the resaearch below, create a structured article outline.
    Return only valid JSON, nothing else.
    
    Research summary: {research_summary} 
    key points: {key_points}
    
    Return JSON with exactly these keys:
    - title: a compelling title for the article
    - sections: a list of 4-5 objects
    
    Each section  object should must contain:
    - heading: a clear section heading
    - key_points: a list of 2-3 short points
    
    Do not add any other keys."""
    )
    
    chain = prompt | llm | JsonOutputParser()
    
    result = chain.invoke({
        "research_summary": research_data["research_summary"],
        "key_points": research_data["key_points"]
    })
    
    return result