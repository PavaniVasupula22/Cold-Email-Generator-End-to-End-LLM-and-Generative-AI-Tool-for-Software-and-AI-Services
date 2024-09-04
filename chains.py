import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        # Initialize the language model with specific parameters.
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(temperature=0, groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")

    def extract_jobs(self, page_text):
        # Template for extracting job information from scraped data.
        extraction_template = PromptTemplate.from_template(
            """
            ### WEBSITE TEXT CONTENT:
            {scraped_text}
            ### TASK:
            The text provided is from a website's careers section.
            Your task is to identify job postings and return them in JSON format. The JSON should include: `role`, `experience`, `skills`, and `description`.
            Ensure only valid JSON is returned.
            ### OUTPUT JSON FORMAT:
            """
        )

        # Combine prompt with the language model.
        extraction_chain = extraction_template | self.llm

        # Execute the extraction process.
        response = extraction_chain.invoke(input={"scraped_text": page_text})

        try:
            # Parse the output to JSON format.
            json_parser = JsonOutputParser()
            jobs = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException("Error: The content is too large to parse. Unable to extract job details.")

        # Ensure the result is a list of job postings.
        return jobs if isinstance(jobs, list) else [jobs]

    def generate_cold_email(self, job_details, portfolio_links):
        # Template for generating a cold email based on job details.
        email_template = PromptTemplate.from_template(
            """
            ### JOB INFORMATION:
            {job_info}

            ### TASK:
            You are representing Company XYZ, an AI & Software Consulting firm specializing in automating business processes. XYZ has a proven track record of delivering customized solutions that drive scalability, optimize processes, reduce costs, and improve overall efficiency.
            Your task is to compose a cold email directed at the client, detailing how XYZ can meet their needs as described in the job posting above.
            Additionally, incorporate relevant links from the following list to highlight the company's portfolio: {portfolio_links}
            
            ### CRAFTED EMAIL:
            """
        )

        # Combine prompt with the language model.
        email_chain = email_template | self.llm

        # Generate the email.
        response = email_chain.invoke({"job_info": str(job_details), "portfolio_links": portfolio_links})
        return response.content

if __name__ == "__main__":
    # Print the API key to verify it's loaded correctly.
    print(os.getenv("GROQ_API_KEY"))
