import os
import time

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from streamlit_option_menu import option_menu
from PIL import Image


# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Chat with Chat.AI!",
    page_icon=":brain:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

system_prompt = """ Hello! Iam AI chatbot named "Chat.AI" created by Dhvanil Patel. I am here to assist you with a wide range of queries, including providing answers to questions, offering suggestions, and helping with coding and processes. "

"Provide only necessary and asked information when someone says hello to you and please keep in mind that you are AI Chat bot Created by Dhvanil not Gemini and be polite and use emoji when some one ask about you, i.e. Hello, Who are you, What is you Name, etc., just give your name and who developed you etc. Here are a few things to keep in mind while using this chatbot:"

"1. **General Assistance**: - I can help with questions from various industries, whether it's technology, healthcare, finance, education, or any other field. - Feel free to ask me about historical events, scientific facts, general knowledge, or specific industry-related information." 

"2. **Coding Help**: - If you need help with programming, debugging, or understanding code, feel free to ask." 
"I support multiple programming languages including Python, JavaScript, Java, C++, and more."
"I can provide code snippets, explanations, best practices, and help you troubleshoot errors in your code."

"3. **Process Guidance**: - I can guide you through different processes, be it project management, software development life cycles, business operations, or other workflows."
"If you're working on a project, I can help you outline steps, identify best practices, and provide templates for documentation." 

"4. **Suggestions and Recommendations**: - I can offer advice and recommendations based on your needs, whether it's related to career, education, project planning, or any other topic." 
"You can ask for book recommendations, study tips, career advice, or suggestions for tools and software to use for various tasks." 

"5. **Learning and Development**: - I can assist with learning new skills, whether it's a new programming language, a technical concept, or soft skills like communication and leadership. Ask me for tutorials, learning paths, or resources to help you grow in your career or personal development."""

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":

        return "assistant"
    elif user_role == "user":
        return user_role
    else:
        None

profile_pic = "D:\Chat.AI\assests\Dp (Main).gif"
css_file = "D:\Chat.AI\styles\main.css"

PAGE_TITLE = "Digital CV | Dhvanil Patel"
PAGE_ICON = ":wave:"
NAME = "Dhvanil Patel"
DESCRIPTION = """
Google Certified Data Analyst | Aspiring Data Scientist | Transforming Insights into Action.

"""
EMAIL = "dhwanil.2301@gmail.com"
LinkedIn = "www.linkedin.com/in/dhvanil-v-patel/"


# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Add the system prompt to the chat history
if "system_prompt_sent" not in st.session_state:
    st.session_state.chat_session.send_message(system_prompt)
    st.session_state.system_prompt_sent = True

with st.sidebar:
    selected = option_menu(
        menu_title= "Main Menu",
        options=["Home", "Let's Connect"],
        icons= ['house', 'envelope'],
        menu_icon='cast',
        default_index=0
    )

if selected == "Let's Connect":
    st.subheader("👋 Hello...!")

    with open(css_file) as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)
    profile_pic = Image.open(profile_pic)

    col1, col2 = st.columns(2, gap="small")
    with col1:
        st.image(profile_pic, width=230)

    with col2:
        st.title(NAME)
        st.write(DESCRIPTION)
        st.write("📩", EMAIL)
        st.write("👨‍⚖️", LinkedIn)

    st.subheader("Your Valuable Feedback Accepted...💭")

    contact_form = """
    <form action="https://formsubmit.co/dhvanil.megascale@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here"></textarea>
        <button type="submit">Send</button>
    </form>
    """
    # contact_form_1 = """<form id="contactform" action="https://formsubmit.io/send/put your email here" method="POST">
    #     <input name="name" type="text" id="name">
    #     <input name="email" type="email" id="email">
    #     <textarea name="comment" id="comment" rows="3"></textarea>
    #     <input name="_formsubmit_id" type="text" style="display:none">
    #     <input value="Submit" type="submit">
    # </form>
    # """

    st.markdown(contact_form, unsafe_allow_html=True)

    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css("D:\Chat.AI\styles\style.css")

if selected == "Home":
    # Display the chatbot's title on the page
    st.header("🤖 Chat.AI")

    # Display the chat history
    for message in st.session_state.chat_session.history:
        if message.parts[0].text != system_prompt:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(message.parts[0].text)

    # Input field for user's message
    user_prompt = st.chat_input("Ask me your question")
    if user_prompt:
        # Add user's message to chat and display it
        st.chat_message("user", avatar= "🙎🏻‍♂️").markdown(user_prompt)

        # Send user's message to Gemini-Pro and get the response
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        
            # Display Gemini-Pro's response
        with st.chat_message("assistant", avatar="🤖"):
             st.markdown(gemini_response.text)


