from neo4j import GraphDatabase
import re
from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests 


app = Flask(__name__) 
api = Api()







class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
            
   
    def find_all_conection(self,node):
        with self.driver.session() as session:
            result = session.read_transaction(self._find_and_return_conections, node)
            return result 
        
    @staticmethod
    def _find_and_return_conections(tx, parametr):
        query= (
            "MATCH (p1:Parametr { id: $parametr })-[r]->()"
            "RETURN r.name"
        )
        result = tx.run(query, parametr=parametr)
        return [re.findall(r"'\w*'",str(row)) for row in result]
    
    def clean_list_conection(self,node):
        list1=self.find_all_conection(node)
        list2=[]
        for i in range(len(list1)):
            if list1[i]:
                list2.append(re.sub(r"'","",list1[i][0]))
                
        return list2

    
    def find_the_next_id(self, priv_id, con_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._find_and_return_the_next_id ,priv_id, con_name)
            return (result[0]['p2'])
    
    @staticmethod 
    def _find_and_return_the_next_id(tx, priv_id, con_name):
        query = (
            
            "MATCH (p1:Parametr {id: $priv_id})-[:KNOWS{name: $con_name}]->(p2)"
            "RETURN p1,p2"
            
        )
        
        result = tx.run(query, priv_id=priv_id, con_name=con_name)
        return [{"p1": row["p1"]["id"], "p2": row["p2"]["id"]}
                for row in result]
        
    
    
    
    def find_a_parametr(self, some_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._find_a_parametr_return ,some_id)
            return (result[0])
    
    @staticmethod 
    def _find_a_parametr_return(tx, some_id):
        query = (
            
            "MATCH (p1:Parametr {id: $some_id})"
            "RETURN p1"
            
        )
        
        result = tx.run(query, some_id=some_id)
        return [row["p1"]["name"]
                for row in result]
    
    def is_a_product(self, some_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._is_a_product_return ,some_id)
            return (result)
    
    @staticmethod 
    def _is_a_product_return(tx, some_id):
        query = (
            
            "MATCH (p1:Product {id: $some_id})"
            "RETURN p1"
            
        )
        
        result = tx.run(query, some_id=some_id)
        return [row["p1"]["name"]
                for row in result]
    
    
    priveos_id=0
    
    def find_c(self,a,b):
        k=''
        for item1 in a:
            for item2 in b:
                if item1==item2:
                   k=item1 
            if k!='':
                break
        return(k)
   
    def find_a_product(self, info):
        self.priveos_id=0
        parametrs=info['normalize'][2:-2].split("', '")
        product1=''
        while True:
            list_of_conections=self.clean_list_conection(self.priveos_id)
            c=self.find_c(parametrs,list_of_conections)
            
            
            if c!='':
                self.priveos_id=self.find_the_next_id(self.priveos_id, c)
            elif len(list_of_conections)==0:
                product1=self.is_a_product(self.priveos_id)
                break
            
            elif c=='' and len(list_of_conections)!=0:
                if len(list_of_conections)==1:
                    self.priveos_id=self.find_the_next_id(self.priveos_id, list_of_conections[0])
                else:
                    product1={self.find_a_parametr(self.priveos_id): ','.join(list_of_conections)}#словарь, где ключ - название параметра, а значение - список вариантов 
                    break
        return product1
    
uri = "neo4j+s://bbeb0756.databases.neo4j.io"
user = "neo4j"
password = "3IPJC0vv5ty1IOcVeyCbW0ZLFzEfwfL0rWXfhaGel1k"
app2= App(uri, user, password)


itog={} 
#сервер
class Main(Resource):
    def get(self,user_id,id):
        global app2
        
        
        
        return itog[id]
        
    def post(self,user_id,id):
        parser = reqparse.RequestParser()
        parser.add_argument("user_id",type = int)
        parser.add_argument("text",type = str)
        parser.add_argument("normalize",type = str)
        parser.add_argument("keywords",type =str)
        itog[id] = parser.parse_args()
        
        #ищем в сетке
       
        
        if type(app2.find_a_product(itog[id]))==dict:
            itog[id]['result']=''
            a=app2.find_a_product(itog[id])  
            str_q=''
            for key in a.keys():
                str_q=key+':'+ str(a[key])
            itog[id]['extra_question']= str_q
           
        else:
            itog[id]['result']=app2.find_a_product(itog[id]) 
            itog[id]['extra_question']=""
            
    
    
    
    
        url2="http://127.0.0.1:3003/api/extra_question/"+str(user_id)+'/'+str(id)    
        requests.post(url2,itog[id])
        return itog.json()
api.add_resource(Main,"/api/net_walker/<int:user_id>/<int:id>")
api.init_app(app)
app.run(debug=True, port=3002, host='127.0.0.1')
app2.close()

    









