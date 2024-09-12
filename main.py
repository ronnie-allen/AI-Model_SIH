import fitz  # PyMuPDF for reading PDFs
from docx import Document  # For reading .docx files
from langchain_ollama import OllamaLLM

# Initialize the Ollama model
try:
    llm = OllamaLLM(model="gemma2:2b")
except Exception as e:
    print("Error initializing OllamaLLM. Ensure that the model is available and properly configured.")
    raise e

# Store user memory (past user inputs)
user_memory = []

# Function to extract text from a .docx file
def read_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""

# Function to extract text from a .pdf file
def read_pdf(file_path):
    try:
        doc = fitz.open(file_path)  # Open PDF with PyMuPDF
        text = ""
        for page in doc:
            text += page.get_text("text")
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""

# Function to get the chat prompt using only user input (memory) and current question
def get_chat_prompt(user_inputs, student_query, document_content=None):
    # Create a basic memory-based context with key past user inputs
    memory_context = ""
    if user_inputs:
        memory_context = "The student has mentioned the following points earlier:\n"
        for user_input in user_inputs:
            memory_context += f"- {user_input}\n"
    
    # Add the current question
    conversation = memory_context + f"Student: {student_query}\n"

    # If document content is provided, append it to the conversation context
    if document_content:
        conversation += f"Here is some useful information from the provided document:\n{document_content}\n"

    # Instruction for career guidance
    conversation += "You are a career counselor for school students. Guide the student based on their interests, memory, and provide career path suggestions, necessary skills, and subjects to focus on."

    return conversation

# Function to generate a career guidance response
def generate_career_guidance(student_query, document_content=None):
    try:
        # Create the prompt from user memory and current query
        prompt = get_chat_prompt(user_memory, student_query, document_content)
        print(f"Generated prompt with memory:\n{prompt}\n")

        # Generate the response using the OllamaLLM model
        response = llm(prompt)

        # Store only the user query in memory, not the entire conversation
        user_memory.append(student_query)

        return response
    except Exception as e:
        print("Error in generating the career guidance response.")
        raise e

# Main function to handle chat and document reading
if __name__ == "__main__":
    try:
        # Variable to hold document content
        document_content = ""
        
        # Ask the user if they want to read a document
        file_option = input("Do you want to read from a document (docx or pdf)? Enter 'yes' or 'no': ").strip().lower()

        if file_option == 'yes':
            file_path = input("Enter the file path (with extension .docx or .pdf): ").strip()
            if file_path.endswith(".docx"):
                document_content = read_docx(file_path)
                print(f"Document content from {file_path}:\n{document_content[:500]}...")  # Preview document content
            elif file_path.endswith(".pdf"):
                document_content = read_pdf(file_path)
                print(f"Document content from {file_path}:\n{document_content[:500]}...")  # Preview document content
            else:
                print("Unsupported file format. Please provide a .docx or .pdf file.")
        
        while True:
            student_query = input("You (Student): ")
            
            # Exit the loop if the student wants to end the conversation
            if student_query.lower() in ["exit", "quit"]:
                print("Exiting chat...")
                break

            # Get the response for career guidance, including document content if available
            response = generate_career_guidance(student_query, document_content)

            print(f"AI (Counselor): {response}\n")
    except Exception as e:
        print(f"An error occurred: {e}")
