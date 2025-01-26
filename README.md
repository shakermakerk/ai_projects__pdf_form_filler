# PDF Form Filler

An automated tool for filling PDF forms programmatically.

## Overview

This Python-based tool automates the process of filling PDF forms, reducing manual data entry work and ensuring consistency in form processing.

## Project Structure

```
.
├── src/
│   └── main.py          # Main application code
├── tests/
│   └── test_form_filler.py  # Test suite
├── inputs/
│   ├── OoPdfFormExample.pdf # Original PDF forms
│   └── filled/             # Directory for processed forms
└── .env.example           # Environment variables template
```

## Features

- Automated PDF form filling using OpenAI gpt-4o-mini
- Smart field matching based on provided knowledge
- Logging system for tracking operations
- Automatic output directory management
- Error handling and validation

## Known Bugs / issues

- Cannot fill in checkboxes
- Cannot fill in dropdown fields
- May generate haluncinated data for some fields

## Getting Started

1. Clone the repository
2. Install required dependencies:
   ```bash
   pip install PyPDF2 openai python-dotenv
   ```
3. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
4. Place PDF forms in the `inputs/` directory
5. Create a `knowledge.txt` file with the information to fill in the forms

## Usage

1. Prepare your knowledge base:
   - Create a `knowledge.txt` file with information about the person
   - Use markdown headers to group information into context groups

2. Run the application:
   ```bash
   python src/main.py
   ```

The script will:
- Read the form fields from your PDF
- Use OpenAI's GPT-3.5 to match knowledge to form fields
- Generate a filled PDF in the `inputs/filled/` directory

## Testing

Run tests using:
```bash
python -m pytest tests/
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the terms to be determined.
