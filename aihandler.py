import os
import dotenv
from mistralai import Mistral

dotenv.load_dotenv()

class LLMInterface:
    def __init__(self):
        self.api_key = os.getenv("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError("MISTRAL_API_KEY not found in environment variables.")
       
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=self.api_key)
   
    def generate_response(self, grades_data):
        """Generates AI insights based on student grades."""
        prompt = f"""
        The following are the academic grades of a student across various modules:


        {grades_data}


        Provide insights and suggest areas for improvement.
        """
        
        try:
            response = self.client.chat.complete(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )


            return response.choices[0].message.content
       
        except Exception as e:
            return f"Error: Failed to fetch AI response. ({str(e)})"