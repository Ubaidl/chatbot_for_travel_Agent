import streamlit as st
from langchain.chains import ConversationChain
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Set up API key for the Groq model
load_dotenv()

# Retrieve the API key from environment variables
myapikey = os.getenv("API_KEY")





#Initialize the Groq client using LangChain with correct initialization
llm = ChatGroq(
    model_name="mixtral-8x7b-32768",  # Model name for Groq
    #api_key=myapikey,
    api_key=myapikey,
    temperature=0.7  # Set temperature for creativity
)

# Initialize LangChain conversation chain
conversation = ConversationChain(llm=llm)

# Streamlit page setup
st.title("Chatbot for Travel Agents")
st.write("Plan your perfect trip by chatting with our assistant!")

# Initialize session states for inputs and chat history
if 'destination' not in st.session_state:
    st.session_state.destination = None
if 'days' not in st.session_state:
    st.session_state.days = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    if message['role'] == 'user':
        st.write(f"**You**: {message['content']}")
    else:
        st.write(f"**Assistant**: {message['content']}")

# Destination input
if st.session_state.destination is None:
    destination = st.text_input("Where would you like to travel?", "")
    if st.button("Submit Destination"):
        if destination:
            st.session_state.destination = destination
            st.session_state.chat_history.append({"role": "user", "content": f"I want to travel to {destination}."})
        else:
            st.write("Please provide a destination.")

# Days input
if st.session_state.destination and st.session_state.days is None:
    days = st.text_input(f"For how many days are you planning to trip to {st.session_state.destination}?", "")
    if st.button("Submit Days"):
        if days.isdigit():
            st.session_state.days = days
            st.session_state.chat_history.append({"role": "user", "content": f"I want to travel to {st.session_state.destination} for {days} days."})

            # Use PromptTemplate to structure the prompt
            prompt_template = PromptTemplate(
                input_variables=["destination", "days"], 
                template="User wants to travel to {destination} for {days} days. Provide a recommendation."
            )

            # Generate the prompt using the input values
            prompt = prompt_template.format(destination=st.session_state.destination, days=st.session_state.days)

            # Integrate LangChain conversation with Groq API
            response = conversation.run(input=prompt)

            # Display the assistant's response
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.write(f"**Assistant**: {response}")
        else:
            st.write("Please provide a valid number for days.")

# Reset Button (Optional)
if st.button("Reset Conversation"):
    st.session_state.destination = None
    st.session_state.days = None
    st.session_state.chat_history = []  # Clear chat history
    st.write("Conversation reset.")
