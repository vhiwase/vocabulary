import requests
from bs4 import BeautifulSoup
import pyttsx3
import re
from PIL import Image
from urllib.request import urlretrieve
import shutil
import os


def regexengine(definition):
    match = re.search("[a-zA-Z0-9. ]+", definition[::-1])
    span = match.span()
    definition = definition[::-1][span[0]:span[1]][::-1].strip()
    return definition


def scrape_vocabulary_com(word):
    # Scrape the vocabulary.com website for the given word
    url = f"https://www.vocabulary.com/dictionary/{word}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract the definition, example sentence, and etymology of the word
    definition = soup.find(class_="definition")
    if definition:
        definition = definition.text
    else:
        definition = "Not Available"
    definition = regexengine(definition)
    pos = soup.find(class_="pos-icon")
    if pos:
        pos = pos.text
    else:
        pos = "Not Available"
    example_sentence = soup.find(class_="example")
    if example_sentence:
        example_sentence = example_sentence.text
    else:
        example_sentence = "Not Available"
    example_sentence = example_sentence.replace('\n', '')
    etymology = soup.find(class_="etymology")
    if etymology:
        etymology = etymology.text
    else:
        etymology = "Not Available"

    # Return the extracted data as a dictionary
    return {
      "word": word,
      "pos": pos,
      "definition": definition,
      "example_sentence": example_sentence,
      "etymology": etymology
    }


def get_random_word():
    # Make a request to the Random Word API to get a random word
    response = requests.get('https://random-word-api.herokuapp.com/word?number=1')
    
    # Convert the response to a json object
    data = response.json()
    
    # Return the first word in the list
    return data[0]


def suggest_vocabulary_word():
    # Choose a random word from the vocabulary object
    vocabulary_word = get_random_word()
    
    vocabulary = scrape_vocabulary_com(vocabulary_word)
    # Look up the meaning, example sentence, and etymology of the chosen word
    meaning = vocabulary["definition"].capitalize()
    pos = vocabulary["pos"].capitalize()
    example_sentence = vocabulary["example_sentence"].capitalize()
    etymology = vocabulary["etymology"].capitalize()
    
    # Suggest the chosen vocabulary word to the user
    text1 = f"Today's vocabulary word is: <strong>{vocabulary_word}</strong>"
    print(text1)
    text2 = f"Part of Speech: <strong>{pos}</strong>"
    print(text2)
    text3 = f"Meaning: <strong>{meaning}</strong>"
    print(text3)
    text4 = f"Example sentence: <strong>{example_sentence}</strong>"
    print(text4)
    text5 = f"Etymology: <strong>{etymology}</strong>"
    print(text5)
    
    return text1, text2, text3, text4, text5, vocabulary_word, pos, meaning, example_sentence, etymology


def pronounciation(vocabulary_word):
    engine = pyttsx3.init() # object creation
    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    new_rate = 160
    engine.setProperty('rate', new_rate)     # setting up new voice rate
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    # engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    engine.say(vocabulary_word)
    engine.runAndWait()
    # engine.save_to_file('{}'.format(vocabulary_word), 'static/pronounciation.mp3')
    engine.stop()


def audio(text1, text2, text3, text4, text5):
    engine = pyttsx3.init() # object creation
    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    new_rate = 160
    engine.setProperty('rate', new_rate)     # setting up new voice rate
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
    # engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
    text1 = text1.replace('</strong>', '').replace('<strong>', '')
    text2 = text2.replace('</strong>', '').replace('<strong>', '')
    text3 = text3.replace('</strong>', '').replace('<strong>', '')
    text4 = text4.replace('</strong>', '').replace('<strong>', '')
    text5 = text5.replace('</strong>', '').replace('<strong>', '')
    engine.say(text1)
    engine.say(text2)
    engine.say(text3)
    engine.say(text4)
    engine.say(text5)
    engine.runAndWait()
    # """Saving Voice to a file"""
    # On linux make sure that 'espeak' and 'ffmpeg' are installed
    # engine.save_to_file('{}\n{}\n{}\n{}\n{}'.format(text1, text2, text3, text4, text5), 'static/audio.mp3')
    # engine.runAndWait()
    engine.stop()
    return text1, text2, text3, text4, text5


def vocabulary_word_search(vocab_word):
    # Use the Google Images API to search for images of the vocabulary word
    url = f"https://www.google.com/search?q={vocab_word}&tbm=isch"
    response = requests.get(url)
    
    # Parse the HTML of the search results page
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find the image URLs in the search results
    image_urls = []
    for img in soup.find_all("img"):
        if img["src"].startswith('https://'):
            image_urls.append(img["src"])
    
    # Download and save the images to your local machine
    for i, image_url in enumerate(image_urls):
        urlretrieve(image_url, f"static/{i}.jpg")
        img = Image.open(f"static/{i}.jpg")
        rgb_im = img.convert("RGB")
        rgb_im.save(f"static/{i}.jpg")



# def output_html(text1, text2, text3, text4, text5, vocabulary_word):    
#     vocabulary_word_search(vocabulary_word)
#     # Open the HTML file in write mode
#     with open("templates/index.html", "w") as file:
#         # Write the HTML structure to the file
#         file.write("<html>\n")
#         file.write("<head>\n")
#         file.write("<title>Vocabulary</title>\n")
#         file.write("</head>\n")
#         file.write("<body>\n")
        
#         # Add the text and images to the body
#         file.write("<div>\n")
#         file.write(f"<p>{text1}</p>\n")
#         file.write(f"<div class='audio-container'><audio src='pronounciation.mp3' controls>Your browser does not support the audio element.</audio></div>")
#         file.write(f"<p>{text2}</p>\n")
#         file.write(f"<p>{text3}</p>\n")
#         file.write(f"<p>{text4}</p>\n")
#         file.write(f"<p>{text5}</p>\n")
#         file.write(f"<p></p>\n")
#         for i in range(20):
#             try:
#                 file.write(f"<img src='{i}.jpg' width='100' height='100'>\n")
#             except:
#                 continue    
#         file.write("</div>\n")
        
#         # Close the HTML structure
#         file.write("</body>\n")
#         file.write("</html>\n")


def main():
    # Suggest a vocabulary word to the user
    folder = 'static'
    # Delete the folder and all of its contents
    os.makedirs(folder, exist_ok=True)
    shutil.rmtree(folder)
    os.makedirs(folder, exist_ok=True)
    text1, text2, text3, text4, text5, vocabulary_word, pos, meaning, example_sentence, etymology = suggest_vocabulary_word()
    # output_html(text1, text2, text3, text4, text5, vocabulary_word)
    audio(text1, text2, text3, text4, text5, vocabulary_word)
    

if __name__ == "__main__":
    main()
