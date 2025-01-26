import json
from src.main import fill_form_from_knowledge

# Example 1: Basic personal information
knowledge1 = """
John lives at 123 Main Street in Sampleville, a charming place known for its vibrant community. 
His residence is marked as house number 45, and he resides in a cosy apartment labelled Apt 12B. 
The area is identified by the postcode 12345. John stands at an impressive height of 175 cm.
"""

# Example 2: Different person with different details
knowledge2 = """
Sarah Johnson resides at 789 Oak Avenue in Rivertown. She lives in house number 22.
Her apartment number is 3A, and her area's postal code is 54321.
Sarah is 165 centimeters tall.
"""

def test_form_filling():
    pdf_path = "/Users/chriswood/Downloads/EDIT OoPdfFormExample.pdf"
    
    print("Testing with first knowledge set...")
    result1 = fill_form_from_knowledge(pdf_path, knowledge1, "filled_form1.pdf")
    if result1['success']:
        print("Success! Form 1 filled with data:")
        print(json.dumps(result1['form_data'], indent=2))
    else:
        print(f"Error with form 1: {result1['error']}")
    
    print("\nTesting with second knowledge set...")
    result2 = fill_form_from_knowledge(pdf_path, knowledge2, "filled_form2.pdf")
    if result2['success']:
        print("Success! Form 2 filled with data:")
        print(json.dumps(result2['form_data'], indent=2))
    else:
        print(f"Error with form 2: {result2['error']}")

if __name__ == "__main__":
    test_form_filling()
