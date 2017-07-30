import requests
import json

class Instant(object):
    def __init__(self, access_token, author_name):
        self.content = []
        self.access_token = access_token
        self.author_name = author_name
    
    def add_tag(self, tag, children=[], append=True, href=None, src=None):    
        d = {"tag": tag}

        if children != []:
            if isinstance(children, str):
                d["children"] = [children]
            elif isinstance(children, list):
                d["children"] = children
            else:
                raise TypeError("'children' must be list or str")
        
        if href or src != None:
            d["attrs"] = {}
        
        if href != None:
            d["attrs"]["href"] = href
        
        if src != None:
            d["attrs"]["src"] = src
        
        if append:
            self.content.append(d)
        else:
            return d
        
    def dump(self):
        return json.dumps(self.content, ensure_ascii=False)
    
    def clear(self):
        self.content = []

    def createPage(self, title, return_content=True, debug=False):
        res = requests.get("https://api.telegra.ph/createPage?access_token={}&title={}&author_name={}&content={}&return_content={}".format(
            self.access_token, title, self.author_name, self.dump(), str(bool(return_content)).lower()
        ))

        if debug:
            print(res.url)
            print(self.dump())

        try:
            return res.json()
        except:
            return res.text