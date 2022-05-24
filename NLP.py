from rutermextract import TermExtractor
import nltk
import pymorphy2
from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests

app = Flask(__name__) 
api = Api()
keyitog={}

class Main(Resource):
    def get(self,user_id,id):
        keyitog[id]['normalize']=str(normalize(keyitog[id]['text']))
        keyitog[id]['keywords']=str(keywords(keyitog[id]['text']))
        if id==0:
            numbers=[x for x in keyitog.keys() if keyitog[x]['user_id'] == user_id]
            itog2={}
            for i in numbers:
                itog2[i]=keyitog[i]
            return itog2
        else:
            
            return keyitog[id]
        
    def post(self,user_id,id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id",type = int)
        parser.add_argument("text",type = str)
        keyitog[id] = parser.parse_args()
        url="http://127.0.0.1:3002/api/net_walker/"+str(user_id)+'/'+str(id)
        self.get(user_id,id)
        requests.post(url,keyitog[id])
        
        return keyitog.json()
    
def normalize(sent):

    words=nltk.word_tokenize(sent)
    normalized_words=[]
    morph = pymorphy2.MorphAnalyzer()
    
    for word in words:
        normalized_words.append(morph.parse(word)[0].normalized.word)
    
    stop=nltk.corpus.stopwords.words('russian')
    words2_2=[item for item in normalized_words if item not in stop]
    
    return(words2_2)

def keywords(sent):
   term_extractor = TermExtractor() 
   a=[]
   for term in term_extractor(sent):
       a.append(term.normalized) 
   return a

api.add_resource(Main,"/api/keywords/<int:user_id>/<int:id>")
api.init_app(app)
app.run(debug=True, port=3001, host='127.0.0.1')
