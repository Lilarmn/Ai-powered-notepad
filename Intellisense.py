import re
from datetime import datetime
from GptApi import SendRequestToAPi


def getDate(text):
    current_date = datetime.now().strftime("%Y-%m-%d")
    updated_text = re.sub(r'#date#', current_date, text)
    return updated_text


def summerize(text):
    try:
        match = re.search(r'#summerize:(.*?)#', text)
        if match:
            content = match.group(1)
            result = SendRequestToAPi('summerize', content)
            updated_text = re.sub(r'#summerize:.*?#', result, text)
        else:
            updated_text = text
        return updated_text
    except AttributeError:
        return text
    except Exception as e:
        print(f"Error in summerize: {e}")
        return text


def grammarCheck(text):
    try:
        match = re.search(r'#grammar:(.*?)#', text)
        if match:
            content = match.group(1)
            result = SendRequestToAPi('grammar', content)
            updated_text = re.sub(r'#grammar:.*?#', result, text)
        else:
            updated_text = text
        return updated_text
    except AttributeError:
        return text
    except Exception as e:
        print(f"Error in grammarCheck: {e}")
        return text


def phraseGenerator(text):
    try:
        match = re.search(r'#genText:(.*?)#', text)
        if match:
            content = match.group(1)
            result = SendRequestToAPi('phrase', content)
            updated_text = re.sub(r'#genText:.*?#', result, text)
        else:
            updated_text = text
        return updated_text
    except AttributeError:
        return text
    except Exception as e:
        print(f"Error in phraseGenerator: {e}")
        return text


def textIq(text):
    print("Original text:", text)
    try:
        for func in [getDate, grammarCheck, summerize, phraseGenerator]:
            text = func(text)  # Update text with each function's result
        return text
    except Exception as e:
        print(f"Error in textIq: {e}")
        return text
