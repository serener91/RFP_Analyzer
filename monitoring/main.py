from dotenv import load_dotenv
from langfuse import Langfuse

"""
from langfuse import Langfuse
 
# Create a text prompt
langfuse.create_prompt(
    name="movie-critic",
    type="text",
    prompt="As a {{criticlevel}} movie critic, do you like {{movie}}?",
    labels=["production"],  # directly promote to production
    config={
        "model": "gpt-4o",
        "temperature": 0.7,
        "supported_languages": ["en", "fr"],
    },  # optionally, add configs (e.g. model parameters or model tools) or tags
) 
 
# Initialize Langfuse client
langfuse = Langfuse()
 
# Get current `production` version of a text prompt
prompt = langfuse.get_prompt("movie-critic")
 
# Insert variables into prompt template
compiled_prompt = prompt.compile(criticlevel="expert", movie="Dune 2")
# -> "As an expert movie critic, do you like Dune 2?"

# Raw prompt including {{variables}}. For chat prompts, this is a list of chat messages.
prompt.prompt
 
# Config object
prompt.config

"""

load_dotenv()

# Initialize Langfuse client
langfuse = Langfuse(
    host="http://localhost:3000"
)


def upload_prompt(prompt_id, prompt_text, prompt_label="latest"):
    """
    p_id = prompt name
    text = some prompt texts
    upload_prompt(p_id, text)
    """

    langfuse.create_prompt(
        name=prompt_id,
        type="text",
        prompt=prompt_text,
        labels=[prompt_label],  # "production" "latest"
    )

    print("sucessfully upload prompt!")


def fetch_prompt(prompt_id, label="latest", version=None):

    """
    print(fetch_prompt('budget_extractor', version=1))
    """

    if version is None:
        return langfuse.get_prompt(prompt_id, label=label).compile()

    else:
        return langfuse.get_prompt(prompt_id, version=version).compile()


def list_prompts():

    """
    for i in langfuse.client.prompts.list().data:
    print(i)
    print(i.name)
    """

    return langfuse.client.prompts.list().data


if __name__ == '__main__':
    # for i in list_prompts():
    #     print(i.name)
    #
    # print(fetch_prompt('sfr_summary'))

    upload_prompt(
        prompt_id="sfr_summary",
        prompt_text="""You are an AI designed to analyze structured JSON-formatted text and generate precise summaries in Korean. Your task is to process multiple chunks of text, each containing the following keys:  

- **Page Number**: The page reference for citation.  
- **Content**: The actual text content.  

Each chunk is separated by a ###. The text may be in either Korean or English.  

### **Instructions:**  
1. **Identify Key Information:**  
   - Analyze the given sentences carefully and identify key points marked with prefix: SFR-**.  

2. **Generate a Structured Summary:**  
   - Structure the summary for each key point by listing objectives in headings or sections: 세부내용.
   - Ensure all key points and relevant details are retained while making the response well-organized.
   - Output only the summary itself. If there is no key points, then simply output None  
   - Do not add any external knowledge—strictly use the provided text.  

3. **Cite Sources Properly:**  
   - Always reference the **Page Number** from which the information was derived.  
   - If multiple sources contribute to the summary, list all relevant page numbers. 
   - Citation should be superscripted 

4. **Format for HTML Compatibility:**  
   - Use proper HTML formatting for readability.  
   - Wrap paragraphs in `<p>` tags.  
   - Use `<strong>` for emphasis and `<ul><li>` for lists if needed.  

### **Example Output Format:**  
<ul>  
  <li><strong>SFR-**</strong>: {summary} <sup>p{page}</sup></li>  
  <li><strong>SFR-**</strong>: {summary} <sup>p{page}</sup></li>  
</ul>
Your responses must strictly follow these guidelines.
    
    """
    )
