import fitz  # PyMuPDF for PDF extraction
from langchain_ollama import OllamaLLM

# Initialize the Ollama model
try:
    llm = OllamaLLM(model="gemma2:2b")
except Exception as e:
    print("Error initializing OllamaLLM. Ensure that the model is available and properly configured.")
    raise e

# Function to extract content from the PDF file
def extract_pdf_content(pdf_path):
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()  # Extract text from each page
        return text
    except Exception as e:
        print("Error extracting content from PDF.")
        raise e

# Function to generate detailed report analysis based on medical data
def generate_health_report(pdf_data):
    try:
        # Construct the dynamic prompt based on the extracted data
        prompt = f"""
        You are an AI medical assistant. Analyze the following patient report data and provide detailed medical insights:

        Patient Report Data:
        {pdf_data}

        Based on the above, write a detailed summary as a doctor would. Focus on the following:
        
        1. Glucose Tolerance Test Results
        2. Current condition of the patient (e.g., pre-diabetes, diabetes, normal)
        3. Any necessary medical advice or recommendations based on the glucose levels
        4. A final detailed analysis with a summary of the patient’s health.
        """

        # Generate the content using the model
        response = llm(prompt)
        return response
    except Exception as e:
        print("Error generating the health report.")
        raise e

# Main function to accept the PDF file and generate the report
if __name__ == "__main__":
    try:
        # Specify the path to the uploaded PDF file
        pdf_path = 'report2.pdf'

        # Extract content from the PDF
        extracted_data = extract_pdf_content(pdf_path)

        # Generate the health report based on the PDF data
        health_report = generate_health_report(extracted_data)

        # Output the generated report
        print("\nGenerated Medical Report:\n")
        print(health_report)

    except Exception as e:
        print(f"An error occurred: {e}")
