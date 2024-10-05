
# #Meet Robo: your friend

# #import necessary libraries
# import io
# import random
# import string # to process standard python strings
# import warnings
# import numpy as np
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
# import warnings
# warnings.filterwarnings('ignore')

# import nltk
# from nltk.stem import WordNetLemmatizer
# nltk.download('popular', quiet=True) # for downloading packages

# # uncomment the following only the first time
# #nltk.download('punkt') # first-time use only
# #nltk.download('wordnet') # first-time use only


# #Reading in the corpus
# with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
#     raw = fin.read().lower()

# #TOkenisation
# sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
# word_tokens = nltk.word_tokenize(raw)# converts to list of words

# # Preprocessing
# lemmer = WordNetLemmatizer()
# def LemTokens(tokens):
#     return [lemmer.lemmatize(token) for token in tokens]
# remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
# def LemNormalize(text):
#     return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# # Keyword Matching
# GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
# GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

# def greeting(sentence):
#     """If user's input is a greeting, return a greeting response"""
#     for word in sentence.split():
#         if word.lower() in GREETING_INPUTS:
#             return random.choice(GREETING_RESPONSES)


# # Generating response
# def response(user_response):
#     robo_response=''
#     sent_tokens.append(user_response)
#     TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
#     tfidf = TfidfVec.fit_transform(sent_tokens)
#     vals = cosine_similarity(tfidf[-1], tfidf)
#     idx=vals.argsort()[0][-2]
#     flat = vals.flatten()
#     flat.sort()
#     req_tfidf = flat[-2]
#     if(req_tfidf==0):
#         robo_response=robo_response+"I am sorry! I don't understand you"
#         return robo_response
#     else:
#         robo_response = robo_response+sent_tokens[idx]
#         return robo_response


# flag=True
# print("Nik: My name is Nik. I will answer your queries about Chatbots. If you want to exit, type Bye!")
# while(flag==True):
#     user_response = input()
#     user_response=user_response.lower()
#     if(user_response!='bye'):
#         if(user_response=='thanks' or user_response=='thank you' ):
#             flag=False
#             print("Nik: You are welcome..")
#         else:
#             if(greeting(user_response)!=None):
#                 print("Nik: "+greeting(user_response))
#             else:
#                 print("Nik: ",end="")
#                 print(response(user_response))
#                 sent_tokens.remove(user_response)
#     else:
#         flag=False
#         print("Nik: Bye! take care..")    
        
        






# Import necessary libraries
import random
import string
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.stem import WordNetLemmatizer
import streamlit as st

# Ignore warnings
warnings.filterwarnings('ignore')

# Download NLTK data (quiet=True for background download)
nltk.download('popular', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Reading in the corpus
with open('chatbot.txt', 'r', encoding='utf8', errors='ignore') as fin:
    raw = fin.read().lower()

# Tokenisation
sent_tokens = nltk.sent_tokenize(raw)
word_tokens = nltk.word_tokenize(raw)

# Preprocessing
lemmer = WordNetLemmatizer()

def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

# Keyword Matching
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
GREETING_RESPONSES = ["Hi", "Hey", "*nods*", "Hi there", "Hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)

# Generating response
def response(user_response):
    nik_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]

    if req_tfidf == 0:
        nik_response = "I am sorry! I don't understand you."
    else:
        nik_response = sent_tokens[idx]
    
    sent_tokens.remove(user_response)
    return nik_response


# Streamlit app setup
def main():
    st.title("🤖 Meet Nik: Your Friendly Chatbot!")
    st.write("Ask me anything about chatbots, and I'll do my best to help! Type 'bye' to end the conversation.")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Chat display using a more simplified format
    def display_chat():
        for message in st.session_state.chat_history:
            if message['sender'] == 'user':
                st.markdown(f"<div style='text-align:right;'><strong>You:</strong> {message['text']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align:left;'><strong>Nik:</strong> {message['text']}</div>", unsafe_allow_html=True)

    # Display chat history (will update each time user sends a message)
    display_chat()

    # User input section
    user_input = st.text_input("Type your message here:")

    # Process user input
    if st.button("Send") and user_input:
        user_input = user_input.lower()

        # Append user message to chat history
        st.session_state.chat_history.append({"sender": "user", "text": user_input})

        # If user says "bye", end the conversation
        if user_input == 'bye':
            st.session_state.chat_history.append({"sender": "bot", "text": "Bye! Take care.."})
            display_chat()
            return

        # Generate response
        if user_input in ['thanks', 'thank you']:
            bot_reply = "You're welcome!"
        elif greeting(user_input) is not None:
            bot_reply = greeting(user_input)
        else:
            bot_reply = response(user_input)

        # Append bot reply to chat history
        st.session_state.chat_history.append({"sender": "bot", "text": bot_reply})

        # Refresh chat display
        display_chat()


if __name__ == '__main__':
    main()
