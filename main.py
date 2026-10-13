import http.client
import json
import os 
DATASET_PATH = "SampledDataset/CleanedTrainDataset.tsv"
SEARCH_ARGS = " -site:snopes.com " \
"-site:politifact.com " \
"-site:truthorfiction.com " \
"-site:factcheck.org " \
"-site:fullfact.org "
"-site:apnews.com " \
"-site:uk.reuters.com " \
"-site:healthnewreviews.org "

"""
Get the API key from the APIKEY.txt file.
"""
def get_API_Key():
    if not os.path.exists("APIKEY.txt"):
        raise FileNotFoundError("APIKEY.txt file not found. Please create the file and add your API key.")
    fd = os.open("APIKEY.txt", os.O_RDONLY)
    byte = os.read(fd, 100)
    byte.strip()
    os.close(fd)
    # print(byte.decode("utf-8"))
    return byte.decode("utf-8")

"""
Search the web for the given query using Serper.dev API.
"""
def search_web(query):
    lAPI_KEY = get_API_Key()
    conn = http.client.HTTPSConnection("google.serper.dev")
    payload = json.dumps({
    "q": query + SEARCH_ARGS,
    "gl": "us",
    "hl": "en",
    "num": 10,
    "autocorrect": False
    })
    headers = {
    'X-API-KEY': lAPI_KEY,
    'Content-Type': 'application/json'
    }
    conn.request("POST", "/search", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

def main():
    pass
    # search_web("One antidepressant shown to control weight during 2-year study")
    

if __name__ == "__main__":
    main()



# from ollama import chat

# response = chat(
# model='gemma3:4b',
# messages=[{'role': 'user', 'content': 'Hello'}],
# )
# print(response.message.content)