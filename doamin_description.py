from langchain_ollama import OllamaLLM

# Initialize the Ollama model
try:
    llm = OllamaLLM(model="gemma2:2b")
except Exception as e:
    print("Error initializing OllamaLLM. Ensure that the model is available and properly configured.")
    raise e

# Function to generate output with detailed content focused on the domain for courses
def generate_detailed_paragraph(name, chosen_career, domain, skills_known, description):
    try:
        # Construct the dynamic prompt
        prompt = f"""
        You are an AI career advisor. A student has provided the following details:

        - Name: {name}
        - Chosen Career: {chosen_career}
        - Domain: {domain}
        - Skills Known: {skills_known}
        - Description: {description}

        Based on this, follow the format below. Ensure that each section's paragraph contains a minimum of 300 words. In section 4, focus entirely on the domain ({domain}) for course recommendations without referring to other inputs like skills or description. Be as detailed and crisp as possible with actionable suggestions. Format section 4 as follows:

        1. Start with a greeting and paragraph combining the student's name and the domain ({domain}).
        2. Write a paragraph on the current domain trends based on the user's input for {domain}.
        3. Write a paragraph that combines the skills known ({skills_known}) with the domain and description ({description}). Suggest how they can utilize these skills in the domain.
        4. Provide a detailed paragraph of suggestions focusing **only** on the domain ({domain}) with the following subheadings:
           - **Courses to be chosen**: Provide specific degree-level recommendations like B.Tech, B.Sc, Diploma, and other relevant programs related to the {domain} domain. Do not mention other inputs such as skills or descriptions.
           - **Skills to acquire**: Mention relevant skills to the {domain}, without referencing the user's specific skills.
           - **Other domains to explore**: Suggest related domains that can enhance expertise in {domain}.
        """

        # Generate the content using the model
        response = llm(prompt)
        return response
    except Exception as e:
        print("Error generating the paragraph.")
        raise e

# Main function to accept user inputs and generate the structured output
if __name__ == "__main__":
    try:
        print("Enter the details for career guidance:")

        # Custom input fields
        name = input("Enter your name: ")
        chosen_career = input("Enter your chosen career: ")
        domain = input("Enter your domain (e.g., Technology, Science, Arts): ")
        skills_known = input("Enter the skills you know (e.g., Programming, Data Analysis, Painting): ")
        description = input("Enter a brief description of your goals or vision: ")

        # Generate the career guidance paragraph
        output = generate_detailed_paragraph(name, chosen_career, domain, skills_known, description)

        # Output the generated paragraph in the required format
        print("\nGenerated Career Guidance:\n")
        print(output)

    except Exception as e:
        print(f"An error occurred: {e}")
