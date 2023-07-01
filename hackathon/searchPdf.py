# # # import os
# # # import requests
# # # from serpapi import GoogleSearch
# # # import pandas as pd

# # # def download_pdf(link, filename):
# # #     response = requests.get(link)
# # #     with open(filename, 'wb') as f:
# # #         f.write(response.content)
# # #     print(f'Downloaded PDF from {link} and saved as {filename}')

# # # def search_and_download_pdfs(keyword, num_results=10):
# # #     print(f'Starting search for "{keyword}"...')
# # #     params = {
# # #       "api_key": os.getenv("SERPAPI_KEY"),
# # #       "engine": "google",
# # #       "q": keyword + " filetype:pdf",
# # #       "hl": "en"
# # #     }

# # #     search = GoogleSearch(params)
# # #     results = search.get_dict()

# # #     pdfs = []
# # #     directory = keyword.replace(' ', '_')
# # #     if not os.path.exists(directory):
# # #         print(f'Creating directory "{directory}"...')
# # #         os.makedirs(directory)

# # #     for index, result in enumerate(results['organic_results']):
# # #         if '.pdf' in result['link'] and index < num_results:
# # #             pdf_file = result['link']
# # #             pdfs.append(pdf_file)
# # #             download_pdf(pdf_file, f"{directory}/pdf_file_{index}.pdf")

# # #     df = pd.DataFrame({'PDF Link': pdfs})
# # #     df.to_csv(f'{directory}/SerpApi_PDFs.csv', index=False)
# # #     print(f'Saved CSV with PDF links at {directory}/SerpApi_PDFs.csv')

# # # def main():
# # #     keyword = input("uganda economic growth since 2020")
# # #     search_and_download_pdfs(keyword)

# # # if __name__ == "__main__":
# # #     main()


# # import os
# # import requests
# # from bs4 import BeautifulSoup
# # from googlesearch import search

# # def download_pdf_files(keyword, max_results=10, directory='./pdfs'):
# #     # Create the directory to save the pdf files if it does not exist
# #     os.makedirs(directory, exist_ok=True)

# #     query = keyword + " filetype:pdf"

# #     # Search the web with the keyword
# #     for url in search(query, num_results=max_results):
# #         response = requests.get(url)
        
# #         # Check if the response content type is pdf
# #         if response.headers['content-type'] == 'application/pdf':
# #             # Extract the pdf file name from the url
# #             filename = os.path.basename(url)
            
# #             # Download and save the pdf file
# #             with open(os.path.join(directory, filename), 'wb') as f:
# #                 f.write(response.content)

# # if __name__ == "__main__":
# #     download_pdf_files('Python Machine Learning', max_results=20)


# # import os
# # import re
# # import requests
# # from datetime import datetime
# # from googlesearch import search

# # def sanitize(filename):
# #     return re.sub(r'(?u)[^-\w.]', '', filename)

# # def download_pdf_files(keyword, max_results=10, base_directory='./pdfs'):
# #     # Generate directory name for today's date
# #     today = datetime.today().strftime('%Y-%m-%d')
# #     directory = os.path.join(base_directory, today)
    
# #     # Create the directory to save the pdf files if it does not exist
# #     os.makedirs(directory, exist_ok=True)

# #     query = keyword + " filetype:pdf"

# #     # Search the web with the keyword
# #     for url in search(query, num_results=max_results):
# #         response = requests.get(url)
        
# #         # Check if the response content type is pdf
# #         if response.headers['content-type'] == 'application/pdf':
# #             # Extract the pdf file name from the url and sanitize it
# #             filename = sanitize(os.path.basename(url))
            
# #             # Check if the file already exists
# #             if not os.path.isfile(os.path.join(directory, filename)):
# #                 # Download and save the pdf file
# #                 with open(os.path.join(directory, filename), 'wb') as f:
# #                     f.write(response.content)

# # if __name__ == "__main__":
# #     download_pdf_files('best cryptocoins', max_results=20)
# import os
# import re
# import requests
# from datetime import datetime
# from googlesearch import search

# def sanitize(filename):
#     return re.sub(r'(?u)[^-\w.]', '', filename)

# def download_pdf_files(keyword, max_results=10, base_directory='./pdfs'):
#     # Generate directory name for today's date
#     today = datetime.today().strftime('%Y-%m-%d')
#     directory = os.path.join(base_directory, today)
    
#     # Create the directory to save the pdf files if it does not exist
#     os.makedirs(directory, exist_ok=True)

#     query = keyword + " filetype:pdf"

#     # Search the web with the keyword
#     for url in search(query, num_results=max_results):
#         try:
#             response = requests.get(url, timeout=10)
#         except requests.exceptions.RequestException as err:
#             print(f"Couldn't download file {url}. Error: {err}")
#             continue

#         # Check if the response content type is pdf
#         if response.headers['content-type'] == 'application/pdf':
#             # Extract the pdf file name from the url and sanitize it
#             filename = sanitize(os.path.basename(url))
            
#             # Check if the file already exists
#             if not os.path.isfile(os.path.join(directory, filename)):
#                 try:
#                     # Download and save the pdf file
#                     with open(os.path.join(directory, filename), 'wb') as f:
#                         f.write(response.content)
#                 except Exception as err:
#                     print(f"Couldn't write file {filename}. Error: {err}")
#                     continue

# if __name__ == "__main__":
#     download_pdf_files('economy of uganda', max_results=20)

import os
import re
import requests
from datetime import datetime
from googlesearch import search
import speech_recognition as sr

from TTS import speak
from _approve import _approve


def sanitize(filename):
    return re.sub(r'(?u)[^-\w.]', '', filename)

def count_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    return len(files)

# def get_user_query():
#     r = sr.Recognizer()
#     query = ""
#     try:
#         with sr.Microphone() as source:
#             r.adjust_for_ambient_noise(source)
#             r.energy_threshold = 200
#             r.pause_threshold = 0.5
            
#             speak("what would you like to research about.")
#             audio = r.listen(source, timeout=10)
#             query = r.recognize_google(audio)
#             speak(f"Your query is: {query}")

#     except sr.WaitTimeoutError:
#         print("Timeout error: the speech recognition operation timed out")
#     except sr.UnknownValueError:
#         speak("Sorry, I could not understand your query. Please try again.")
#     except sr.RequestError as e:
#         speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
#     except Exception as e:
#         speak(f"An error occurred: {e}")
    
#     return query
def get_user_query():
    r = sr.Recognizer()
    query = ""
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.energy_threshold = 200
            r.pause_threshold = 0.5
            
            while True:
                speak("What would you like to research about?")
                audio = r.listen(source, timeout=10)
                query = r.recognize_google(audio)
                # speak(f"Your query is: {query}")
                
                approval = _approve(query)  # Add the approval check
                
                if approval:
                    break
                else:
                    speak("Sorry, the query you provided is not approved. Please try again.")
    except sr.WaitTimeoutError:
        print("Timeout error: the speech recognition operation timed out")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand your query. Please try again.")
    except sr.RequestError as e:
        speak(f"Could not request results from the speech recognition service; check your internet connection: {e}")
    except Exception as e:
        speak(f"An error occurred: {e}")
    
    return query

def download_pdf_files( max_results=10, base_directory='./pdfs'):

    keyword = get_user_query()
    # Generate directory name for today's date
    today = datetime.today().strftime('%Y-%m-%d')
    directory = os.path.join(base_directory, today)
    
    # Create the directory to save the pdf files if it does not exist
    os.makedirs(directory, exist_ok=True)

    query = keyword + " filetype:pdf"

    # List to store the names of downloaded files
    downloaded_files = []

    # Search the web with the keyword
    speak("iNITIALIZING DOWNLOADS")
    for url in search(query, num_results=max_results):
        try:
            
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as err:
            print(f"Couldn't download file {url}. Error: {err}")
            continue

        # Check if the response content type is pdf
        if response.headers['content-type'] == 'application/pdf':
            # Extract the pdf file name from the url and sanitize it
            filename = sanitize(os.path.basename(url))
            
            # Check if the file already exists
            if not os.path.isfile(os.path.join(directory, filename)):
                try:
                    # Download and save the pdf file
                    with open(os.path.join(directory, filename), 'wb') as f:
                        f.write(response.content)
                    downloaded_files.append(filename)  # Add the file name to the list
                    speak("DOWNLOADED {filename}")
                except Exception as err:
                    print(f"Couldn't write file {filename}. Error: {err}")
                    continue

    # After downloading all files, print the count and the names
    # speak(f"Downloaded {len(downloaded_files)} files:")
    # speak(f"Downloaded filesnames include :")
    speak(f"Downloaded files successfully")

    # for file_name in downloaded_files:
    #     speak(file_name)

# if __name__ == "__main__":
#     download_pdf_files(max_results=15)
