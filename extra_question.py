from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
 

app = Flask(__name__) # название нашего файла щас main.py
api = Api()
itog={}
class Main(Resource):
    def get(self,user_id,id):
        
        
        return itog[id]
        
    def post(self,user_id,id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id",type = int)
        parser.add_argument("text",type = str)
        parser.add_argument("normalize",type = str)
        parser.add_argument("keywords",type = str)
        parser.add_argument("result",type = str)
        parser.add_argument("extra_question",type = str )
        itog[id] = parser.parse_args()
        
        if itog[id]['result']=='':
            need=itog[id]['extra_question'].split(':')
            itog[id]['extra_question']='В вашем запросе не хватает данных. Пожалуйста укажите этот параметр : ' + need[0]
            itog[id]['extra_values']=str(need[1])
        else:
            itog[id]['extra_values']=''
        
        url="http://127.0.0.1:3000/api/teleg/"+str(user_id)+'/'+str(id)
        requests.put(url,itog[id])
      
        return itog.json()
api.add_resource(Main,"/api/extra_question/<int:user_id>/<int:id>")
api.init_app(app)

app.run(debug=True, port=3003, host='127.0.0.1')



