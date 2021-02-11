from requests import post

def neko(text):

    return ("https://nekobin.com/" + 
        post(
            "https://nekobin.com/api/documents",
            data={"content": text}
            
            ).json()["result"]["key"])