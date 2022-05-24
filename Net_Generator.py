from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import csv
import re


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
            
    
    def find_parametr(self, parametr):
         with self.driver.session() as session:
             result = session.read_transaction(self._find_and_return_parametr, parametr)
             for row in result:
                 return True
    
    @staticmethod
    def _find_and_return_parametr(tx, parametr):
         query = (
             "MATCH (p:Parametr) "
             "WHERE p.name = $parametr "
             "RETURN p.name AS name"
         )
         result = tx.run(query, parametr=parametr)
        
         return [row["name"] for row in result]
   
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
 
    
 
    def create_paramtr(self, parametr, par_id):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_parametr, parametr, par_id)
           
    
    @staticmethod 
    def _create_and_return_parametr(tx, parametr,par_id):
         query = (
             "CREATE (p1:Parametr { name: $parametr, id: $par_id}) "
             "RETURN p1"
         )
         
         result = tx.run(query, parametr=parametr, par_id=par_id)
         return [{"p1": row["p1"]["parametr",'par_id']}
                     for row in result]
    
    def clean_list_conection(self,node):
        list1=self.find_all_conection(node)
        list2=[]
        for i in range(len(list1)):
            if list1[i]:
                list2.append(re.sub(r"'","",list1[i][0]))
                
        return list2
            
    def parametr_list(self):
        with open('проба.csv') as file1:
            reader = csv.reader(file1, delimiter=';')
            row1 = next(reader)
        return row1
    
    def create_new_conections_and_node(self,  node1, node2_name, node2, con_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_new_conections_and_node ,node1, node2_name, node2, con_name)
            return (result[0]['p1'],result[0]['p2'])
    
    @staticmethod 
    def _create_and_return_new_conections_and_node(tx, node1, node2_name, node2, con_name):
        query = (
            "MATCH (p1:Parametr { id: $node1 }) "
            "CREATE (p2:Parametr { name: $node2_name, id: $node2 })"
            "CREATE (p1)-[:KNOWS{name: $con_name}]->(p2)"
            "RETURN p1,p2"
            
        )
        
        result = tx.run(query, node1=node1, node2_name=node2_name,node2=node2, con_name=con_name)
        return [{"p1": row["p1"]["id"], "p2": row["p2"]["id"]}
                for row in result]
    
    def find_the_next_id(self, priv_id, con_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._find_and_return_the_next_id ,priv_id, con_name)
            return (result[0]['p2'])
    
    @staticmethod 
    def _find_and_return_the_next_id(tx, priv_id, con_name):
        query = (
            
            "MATCH (p1:Parametr {id: $priv_id})-[:KNOWS{name: $con_name}]->(p2:Parametr)"
            "RETURN p1,p2"
            
        )
        
        result = tx.run(query, priv_id=priv_id, con_name=con_name)
        return [{"p1": row["p1"]["id"], "p2": row["p2"]["id"]}
                for row in result]
        
    
    def create_product(self, product_name, product_id, priv_id, con_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_product ,product_name, product_id, priv_id, con_name)
            return 
   
    @staticmethod 
    def _create_and_return_product(tx, product_name, product_id, priv_id, con_name):
        query = (
            
            "MATCH (p1:Parametr { id: $priv_id }) "
            "CREATE (p2:Product { name: $product_name, id: $product_id })"
            "CREATE (p1)-[:KNOWS{name: $con_name}]->(p2)"
            "RETURN p1,p2"
        )
        result = tx.run(query,  product_name=product_name, product_id=product_id, priv_id=priv_id, con_name= con_name)
        return [{"p1": row["p1"]["id"], "p2": row["p2"]["id"]}
                for row in result]
    
    
    next_id=0
    id_count=0
    priveos_id=0
    
  
    def make_a_path(self):
        with open('проба.csv') as file1:
            reader = csv.reader(file1, delimiter=';')
            next(reader)
            first_node=False
            parametr_list1=self.parametr_list()
            if first_node==False:
                self.create_paramtr(parametr_list1[2],0)
            first_node=True
            for row in reader:
                self.priveos_id=0
                for i in range(3,len(row)):
                    list_of_conections=self.clean_list_conection(self.priveos_id)
                    
        
                    if str(row[i-1]) not in list_of_conections:
                       
                        self.create_new_conections_and_node(self.priveos_id, parametr_list1[i], self.id_count+1, row[i-1])
                        self.id_count+=1
                        self.priveos_id=self.id_count
                    else:
                        self.priveos_id=self.find_the_next_id(self.priveos_id, row[i-1])
                self.create_product(row[1], row[0], self.priveos_id, row[-1])
        return
            
                
                    
             
         
            
if __name__ == "__main__":    
    uri = "neo4j+s://bbeb0756.databases.neo4j.io"
    user = "neo4j"
    password = "3IPJC0vv5ty1IOcVeyCbW0ZLFzEfwfL0rWXfhaGel1k"
    app = App(uri, user, password)
    app.make_a_path()  
    app.close()
