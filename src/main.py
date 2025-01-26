#!/usr/bin/env python3
from PyPDF2 import PdfReader, PdfWriter
import json
from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_form_fields(pdf_path):
    """Get all form fields from a PDF"""
    try:
        reader = PdfReader(pdf_path)
        return reader.get_form_text_fields()
    except Exception as e:
        logging.error(f"Error reading PDF form fields: {str(e)}")
        raise

def parse_knowledge_with_llm(knowledge, form_fields):
    """Use OpenAI to parse knowledge and match it to form fields"""
    try:
        # Ensure we have an API key
        if not os.getenv('OPENAI_API_KEY'):
            raise Exception("OpenAI API key not found in environment variables")
            
        # Create the prompt for the LLM
        prompt = f"""
        You are provided with detailed knowledge about a person and a list of form fields from a PDF document.
        Your task is to create a JSON object that accurately maps each form field to the corresponding value extracted from the knowledge.
        Ignore any fields that are of type drop down.
        Do not make things up, if you do not know the answer leave the result blank. 
        
        Instructions:
        1. Analyze the provided knowledge to identify relevant information for each form field. Always pay attention to the contect to the knowledge base. markdown headeers are used to group information context groups. 
        2. If a form field cannot be directly matched with the knowledge, assign it an empty string.
        3. Ensure the JSON object is valid and contains all form fields, even if some are empty.
        4. Handle any ambiguities by making reasonable assumptions based on the context provided.
        
        Knowledge about the person:
        {knowledge}
        
        Form fields to fill:
        {json.dumps(list(form_fields.keys()), indent=2)}
        
        Return only a valid JSON object mapping field names to values, nothing else.
        Example format:
        {{
            "Field Name 1": "value1",
            "Field Name 2": "value2"
        }}
        Note: Ensure the JSON is well-formed and includes all fields.
        """
        
        # Get completion from OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts information from text and maps it to form fields. Respond only with valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        # Parse the response
        form_data = json.loads(response.choices[0].message.content)
        return form_data
        
    except Exception as e:
        logging.error(f"Error parsing knowledge with LLM: {str(e)}")
        raise

def fill_pdf_form(input_path, output_path, form_data):
    """Fill PDF form with the provided data"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # Get the first page
        page = reader.pages[0]
        writer.add_page(page)
        
        # Update form fields
        writer.update_page_form_field_values(
            writer.pages[0],
            form_data
        )
        
        # Write the output PDF
        with open(output_path, "wb") as output_file:
            writer.write(output_file)
        
        return True
    except Exception as e:
        logging.error(f"Error filling PDF form: {str(e)}")
        raise

def fill_form_from_knowledge(pdf_path, knowledge, output_path=None):
    """Main function to fill a PDF form using knowledge text"""
    try:
        # If no output path specified, create one based on input
        if output_path is None:
            output_dir = os.path.join('inputs', 'filled')
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(pdf_path).rsplit('.', 1)[0] + '_filled.pdf')
        
        # Get form fields from PDF
        form_fields = get_form_fields(pdf_path)
        
        # Parse knowledge and match to form fields using LLM
        form_data = parse_knowledge_with_llm(knowledge, form_fields)
        
        # Fill the PDF form
        success = fill_pdf_form(pdf_path, output_path, form_data)
        
        logging.info(f"PDF form has been filled and saved to {output_path}")
        return {
            'success': success,
            'output_path': output_path,
            'form_data': form_data
        }
        
    except Exception as e:
        logging.error(f"Error in fill_form_from_knowledge: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

if __name__ == "__main__":
    # Example usage
    pdf_path = "inputs/OoPdfFormExample.pdf"
    # Read knowledge from knowledge.txt
    with open('knowledge.txt', 'r') as file:
        knowledge = file.read()
    fill_form_from_knowledge(pdf_path, knowledge)
