# This file stores additional functions that simplify the main code.
# ----------------
import re

# This function removes all emoji in the title
def deEmojify(text):
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

# This function reads the file and returns its content
def message_from_file(filename):
    with open(filename, "r", encoding='UTF-8') as file:
        content = file.read()
        
        if(len(content) == 0): 
            content = "К сожалению, не могу предоставить информацию 🥲"

        return content