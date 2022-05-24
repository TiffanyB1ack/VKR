from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
app = Flask(__name__) # название нашего файла щас main.py
api = Api()
itog={}
class Main(Resource):
    def get(self,user_id,id):
        

        if id == 0:
            numbers=[x for x in itog.keys() if itog[x]['user_id'] == user_id]
            itog2={}
            for i in numbers:
                itog2[i]=itog[i]
            return itog2
        else:
            return itog[id]
        
    def post(self,user_id,id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id",type = int)
        parser.add_argument("text",type = str)
        itog[id] = parser.parse_args()
        url="http://127.0.0.1:3001/api/keywords/"+str(user_id)+'/'+str(id)
        requests.post(url,itog[id])
        return itog.json()
    
    def put(self,user_id,id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id",type = int)
        parser.add_argument("text",type = str)
        parser.add_argument("normalize",type = str)
        parser.add_argument("keywords",type = str)
        parser.add_argument("result",type = str)
        parser.add_argument("extra_question",type = str)
        parser.add_argument("extra_values",type = str)
        itog[id] = parser.parse_args()
        return itog.json()
    
api.add_resource(Main,"/api/teleg/<int:user_id>/<int:id>")
api.init_app(app)
if __name__ == "__main__":
    app.run(debug=True, port=3000, host='127.0.0.1')

