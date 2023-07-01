import json
from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.memory import ConversationBufferWindowMemory
import os
from dotenv import find_dotenv, load_dotenv
import speech_recognition as sr
import pyttsx3
from datetime import datetime

from TTS import speak
from TTS import wishMe


from _approve import _approve
from TTS import capture_image
from ReadKeras import process_image
from cap import generate_image_captions
from imageCaption import CaptionImage

from newPDFProcess import document_search

dotenv_path= find_dotenv()
load_dotenv(dotenv_path)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

template = """
TOM  is your assistant trained by OpenAI.

TOM  is designed to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics.

TOM is constantly learning and improving. It processes and understands large amounts of text, and uses this knowledge to provide accurate and informative responses.

Be aware that some errors might occur in the transcription of our conversations due to the audio input. TOM will attempt to account for words that may have been misinterpreted due to their similarity in sound.

Here is your conversation history:
{history}

TOM: {human_input}
USER:"""


def save_user_name(user_name):
    with open("user_name.txt", "w") as file:
        file.write(user_name)


def get_user_name():
    if os.path.exists("user_name.txt"):
        with open("user_name.txt", "r") as file:
            return file.read()
    return None


def save_conversation(user_input, bot_response):
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    conversation = {
        "datetime": current_datetime,
        "user_input": user_input,
        "bot_response": bot_response
    }
    conversation_dir = "conversations"
    if not os.path.exists(conversation_dir):
        os.makedirs(conversation_dir)
    file_path = os.path.join(conversation_dir, f"conversation_{current_datetime}.json")
    with open(file_path, "w") as file:
        json.dump(conversation, file)
        
 
def get_names():
    r = sr.Recognizer()
    user_name = get_user_name()
    bot_name = "Tom"
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5
            
            if user_name:
                speak(f"Welcome back, {user_name}!")
            else:
                speak("Hi there. What's your name?")
                audio = r.listen(source, timeout=10, phrase_time_limit=30)
                user_name = r.recognize_google(audio)
                speak(f"Nice to meet you, {user_name}.")
                save_user_name(user_name)
            
           
    except sr.WaitTimeoutError:
        print("Timeout error: the speech recognition operation timed out")
        return get_names()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your input. No worries, let's try that again.")
        return get_names()
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; check your internet connection: {e}")
        return get_names()
    except Exception as e:
        print(f"An error occurred: {e}")
        return get_names()
    return user_name, bot_name


prompt = PromptTemplate(input_variables=[ "history", "human_input"], template=template)
chatgpt_chain = LLMChain(
    llm=OpenAI(temperature=0),
    prompt=prompt,
    verbose=True,
    memory=ConversationBufferWindowMemory(k=2),
)

engine = pyttsx3.init()

def listen():
    r = sr.Recognizer()
    wishMe()
    get_names()

    try:
        speak("hi!, I'm Tom. Feel free to ask me anything.")

        with sr.Microphone() as source:
            speak("Initializing microphone for use...")
            r.adjust_for_ambient_noise(source, duration=5)
            r.energy_threshold = 200
            r.pause_threshold = 0.5

            speak("Okay, let's get started!")
            while True:
                text = ""
                speak("Listening for new input. now...")
                try:
                    audio = r.listen(source, timeout=60, phrase_time_limit=60)
                    speak("Recognizing...")
                    text = r.recognize_google(audio)
                    # Add conditionals for triggering your functions based on the recognized text

                    if 'search' in text.lower():
                        
                        document_search()
                    elif 'caption image' in text.lower():
                        speak("image caption function selected")
                        generate_image_captions()
                    elif 'read' in text.lower():
                        speak("read function selected")
                        process_image()
                       
                    else:
                        approval = _approve(text)
                        if not approval:
                            continue

                except sr.WaitTimeoutError:
                    print("Timeout error: the speech recognition operation timed out")
                    continue
                except sr.UnknownValueError:
                    speak("Could not understand the audio")
                    continue
                except sr.RequestError as e:
                    speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
                    continue
                except Exception as e:
                    speak(f"An error occurred: {e}")
                    continue

                else:
                    speak("Processing your input: " + text)

                    response_text = chatgpt_chain.predict(human_input=text)
                    if response_text.lower() == 'goodbye':
                        speak("See you later!")
                        break
                    speak(response_text)
                    save_conversation(text, response_text)
                engine.runAndWait()
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    listen()

    



