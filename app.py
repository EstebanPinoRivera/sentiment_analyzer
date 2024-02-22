from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("API_KEY")
)
# Defining a system role with instructions for the sentiment analyzer
system_rol = """Actúa como analizador de sentimientos.
                Yo te indico los sentimientos y tu analizas el sentimiento de los mensajes y, me das
                una respuesta con al mens un carater y como máximo 4 caracteres. Solo respuestas númericas, donde -1
                es negatividad máxima, 0 es neutral y 1 es positiidad máxima. Incluye también rangos, es decir, 0.1, -0.4
                etc., también son válidos Puede responder con ints o floats"""
                
# Creating a message list with a system role message
message = [{"role": "system", "content": system_rol}]

# Defining a class to represent sentiments
class Sentiment:
    def __init__(self, name, color):
        self.name = name
        self.color = color
    
    def __str__(self):
        return "\x1b[1;{}m{}\x1b[1;31m".format(self.color, self.name)
    
# Defining a sentiment analyzer class
class SentimentAnalyzer:
    def __init__(self, ranges):
        self.ranges = ranges
    
    def analyze_sentiments(self, polarity):
        for rank, sentiment in self.ranges:
            if rank[0] < polarity <= rank[1]:
                return sentiment
        return Sentiment("Muy negativo", "31")
    
#Defining sentiment ranges and associated sentiments    
ranges = [
    ((-0.7, -0.3),Sentiment("Negativo", "31")),
    ((-0.3, -0.1),Sentiment("Algo negativo", "31")),
    ((-0.1, 0.1),Sentiment("Neutral", "33")),
    ((0.1, 0.4),Sentiment("Algo positivo", "32")),
    ((0.4, 0.9),Sentiment("Positivo", "32")),
    ((0.9, 1),Sentiment("Muy positivo", "32"))   
]

# Creating an instance of the SentimentAnalyzer
analyze = SentimentAnalyzer(ranges)

# Main loop for user interaction
while True:
    user_prompt = input("\x1b[1;33m" + "\nDi algo: " + "\x1b[1;37m")
    message.append({"role": "user", "content": user_prompt})
    
    # Generating a chat completion using the OpenAI API
    chat_completion = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages = message,
        max_tokens = 8
    )
    
    # Retrieving the response from the chat completion
    answer = chat_completion.choices[0].message.content
    message.append({"role": "assistant", "content": answer})
    
    # Analyzing sentiment of the response
    sentiment = analyze.analyze_sentiments(float(answer))
    print(sentiment)