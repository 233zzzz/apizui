#encoding=utf-8
from app import GstoreConnector
#!/usr/bin/env python
#import os
#import unittest
import re
from app import app
from json import dumps
from flask import Flask, g, Response, request,jsonify,abort, make_response
#from neo4j.v1 import GraphDatabase, basic_auth
from py2neo import Graph
#from flask_mysqldb import MySQL
#from neo4j import GraphDatabase
import MySQLdb
gc = GstoreConnector.GstoreConnector("10.168.7.245", 9001)
username = "root"
password = "123456"

#nodes1 = []
links1 = []    #股东边
def queryholderss(names,depth):
    curs = db403.cursor()
    a = []
    for name in names:  #python 字符串连接啊
        sparql = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" +name+"> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
        #print(sparql)
        strr = gc.query(username, password, "holder10", sparql)
        r = strr.split("\n")
        for i in r:
            p = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res = re.findall(p, i)
            result = ''.join(res)
            query = "SELECT * FROM enterprise_copy where name = %s"  #uuid
            param = (result,)
            curs.execute(query, param)
            rvs = curs.fetchall()
            ids = None
            for t in rvs:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p = 0
            if len(result) < 4 and len(result) > 1:
                p = 2
                links1.append({"source": result, "target": name, "relation": "hold"})
                #nodes1.append({"name": result, "type": p,"credit_no":idss,"direction":"up"})

                a.append(result)
            elif len(result) >= 4:
                p = 1
                #nodes1.append({"name": result, "type": p, "credit_no": idss, "direction": "up"})
                links1.append({"source": result, "target": name, "relation": "hold"})
                a.append(result)
            # for x in a:  #同一层边连接
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return links1
    else:
        return queryholderss(a, depth - 1)

#nodes2 = []
links2 = []      #持股边
#print(queryholders(['招商银行股份有限公司'],3))  输入的是一个数组
def queryholderss2(names,depth):
    curs = db403.cursor()
    a = []
    for name in names:  # python 字符串连接啊
        sparql2 = "select distinct * where{ ?x <http://localhost:2020/vocab/resource/holder_copy_holder_name> <file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + name + ">}"
        strr2 = gc.query(username, password, "holder10", sparql2)
        r2 = strr2.split("\n")
        for i2 in r2:
            p2 = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res2 = re.findall(p2, i2)
            result2 = ''.join(res2)

            query2 = "SELECT * FROM enterprise_copy where name = %s"  #查uuid
            param2 = (result2,)
            curs.execute(query2, param2)
            rv2 = curs.fetchall()
            ids = None
            for t in rv2:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #查信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p2 = 0
            if len(result2) < 4 and len(result2) > 1:
                p2 = 2
                #nodes2.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down"})
                links2.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            elif len(result2) >= 4:
                p2 = 1
                #nodes2.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down"})
                links2.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            # for x in a:
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return links2
    else:
        return queryholderss2(a, depth - 1)


nodes3 = []  #股东节点
#links3 = []
#aaa = []
#aaa = 0   #全局变量改变了，不能在这改，每次请求全局变量都不一样了
def queryholders(names,depth):
    curs = db403.cursor()
    #global aaa   #关键  改变全局变量
    #nodes = []
    #links = []
    a = []
    #aaa += 1
    for name in names:  #python 字符串连接啊
        sparql = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" +name+"> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
        #print(sparql)
        strr = gc.query(username, password, "holder10", sparql)
        r = strr.split("\n")
        for i in r:
            p = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res = re.findall(p, i)
            result = ''.join(res)
            query = "SELECT * FROM enterprise_copy where name = %s"  #uuid
            param = (result,)
            curs.execute(query, param)
            rvs = curs.fetchall()
            ids = None
            for t in rvs:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p = 0
            if len(result) < 4 and len(result) > 1:
                p = 2
                #links3.append({"source": result, "target": name, "relation": "hold"})
                if result not in names:  #决定节点是否可以处在不同层级
                    nodes3.append({"name": result, "type": p,"credit_no":idss,"direction":"up","depth":dep-depth+1})

                a.append(result)
            elif len(result) >= 4:
                p = 1
                if result not in names:
                    nodes3.append({"name": result, "type": p, "credit_no": idss, "direction": "up","depth":dep-depth+1})  #dep-depth+1
                #links3.append({"source": result, "target": name, "relation": "hold"})
                a.append(result)
            # for x in a:  #同一层边连接
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return nodes3
    else:
        return queryholders(a, depth - 1)

nodes4 = []   #持股节点
#links4 = []
#bbb = 0
#print(queryholders(['招商银行股份有限公司'],3))  输入的是一个数组
def queryholders2(names,depth):
    curs = db403.cursor()
    #global bbb
    #nodes = []
    #links = []
    a = []
    #bbb += 1
    for name in names:  # python 字符串连接啊
        sparql2 = "select distinct * where{ ?x <http://localhost:2020/vocab/resource/holder_copy_holder_name> <file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + name + ">}"
        strr2 = gc.query(username, password, "holder10", sparql2)
        r2 = strr2.split("\n")
        for i2 in r2:
            p2 = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res2 = re.findall(p2, i2)
            result2 = ''.join(res2)

            query2 = "SELECT * FROM enterprise_copy where name = %s"  #查uuid
            param2 = (result2,)
            curs.execute(query2, param2)
            rv2 = curs.fetchall()
            ids = None
            for t in rv2:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #查信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p2 = 0
            if len(result2) < 4 and len(result2) > 1:
                p2 = 2
                if result2 not in names:
                    nodes4.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down","depth":dep-depth+1})
                #links4.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            elif len(result2) >= 4:
                p2 = 1
                if result2 not in names:
                    nodes4.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down","depth":dep-depth+1})
                #links4.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            # for x in a:
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return nodes4
    else:
        return queryholders2(a, depth - 1)
#print(queryholders2(['招商银行股份有限公司'],2))

nodes5 = []  #股东节点
#links3 = []
#aaa = []
#aaa = 0   #全局变量改变了，不能在这改，每次请求全局变量都不一样了
def queryholders5(names,depth):
    curs = db403.cursor()
    #global aaa   #关键  改变全局变量
    #nodes = []
    #links = []
    a = []
    #aaa += 1
    for name in names:  #python 字符串连接啊
        sparql = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" +name+"> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
        #print(sparql)
        strr = gc.query(username, password, "holder10", sparql)
        r = strr.split("\n")
        for i in r:
            p = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res = re.findall(p, i)
            result = ''.join(res)
            query = "SELECT * FROM enterprise_copy where name = %s"  #uuid
            param = (result,)
            curs.execute(query, param)
            rvs = curs.fetchall()
            ids = None
            for t in rvs:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p = 0
            if len(result) < 4 and len(result) > 1:
                p = 2
                #links3.append({"source": result, "target": name, "relation": "hold"})
                if result not in names:  #决定节点是否可以处在不同层级
                    nodes5.append({"name": result, "type": p,"credit_no":idss,"direction":"up","depth":des-depth+1})

                a.append(result)
            elif len(result) >= 4:
                p = 1
                if result not in names:
                    nodes5.append({"name": result, "type": p, "credit_no": idss, "direction": "up","depth":des-depth+1})  #dep-depth+1
                #links3.append({"source": result, "target": name, "relation": "hold"})
                a.append(result)
            # for x in a:  #同一层边连接
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return nodes5
    else:
        return queryholders5(a, depth - 1)

nodes6 = []   #持股节点
#links4 = []
#bbb = 0
#print(queryholders(['招商银行股份有限公司'],3))  输入的是一个数组
def queryholders6(names,depth):
    curs = db403.cursor()
    #global bbb
    #nodes = []
    #links = []
    a = []
    #bbb += 1
    for name in names:  # python 字符串连接啊
        sparql2 = "select distinct * where{ ?x <http://localhost:2020/vocab/resource/holder_copy_holder_name> <file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + name + ">}"
        strr2 = gc.query(username, password, "holder10", sparql2)
        r2 = strr2.split("\n")
        for i2 in r2:
            p2 = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            res2 = re.findall(p2, i2)
            result2 = ''.join(res2)
            query2 = "SELECT * FROM enterprise_copy where name = %s"  #查uuid
            param2 = (result2,)
            curs.execute(query2, param2)
            rv2 = curs.fetchall()
            ids = None
            for t in rv2:
                if t:
                    ids = t[1]
                else:
                    ids = None
            idss = None
            query11 = "SELECT * FROM enterprise where id = %s"  #查信用码
            param11 = (ids,)
            curs.execute(query11, param11)
            rvss = curs.fetchall()
            for i in rvss:
                if i:
                    idss = i[8]
                else:
                    idss = None
            p2 = 0
            if len(result2) < 4 and len(result2) > 1:
                p2 = 2
                if result2 not in names:
                    nodes6.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down","depth":des-depth+1})
                #links4.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            elif len(result2) >= 4:
                p2 = 1
                if result2 not in names:
                    nodes6.append({"name": result2, "type": p2, "credit_no": idss, "direction": "down","depth":des-depth+1})
                #links4.append({"source": name, "target": result2, "relation": "hold"})
                #nodes.append({"name": result2, "type": p2,"credit_no":idss})
                a.append(result2)
            # for x in a:
            #     spar = "select distinct * where{<file:///F:/d2r-server-0.7/holder8.nt#holder_copy/" + x + "> <http://localhost:2020/vocab/resource/holder_copy_holder_name> ?t}"
            #     # print(sparql)
            #     strp = gc.query(username, password, "holder10", spar)
            #     r3 = strp.split("\n")
            #     for rp in r3:
            #         pp = re.compile(r'[\u4e00-\u9fa5]')  # 提取中文
            #         resl = re.findall(pp, rp)
            #         resul = ''.join(resl)
            #         if resul in nodes:
            #             links.append({"source": resul, "target": x, "relation": "hold"})
    if depth == 1:
        return nodes6
    else:
        return queryholders6(a, depth - 1)

def combine(names,depth):
    return queryholders(names,depth)+queryholders2(names,depth)

def combine5(names,depth):
    return queryholders5(names,depth)+queryholders6(names,depth)

def combine1(names,depth):
    return queryholderss(names,depth)+queryholderss2(names,depth)
#print(combine(['招商银行股份有限公司'],1))

#app = Flask(__name__, static_url_path='/static/')
#dbs = MySQLdb.connect("localhost", "root", "zlj000", "zlj")
db403 = MySQLdb.connect("10.168.7.245", "root", "zhirong123", "business_data_db",charset='utf8')  #utf8处理中文
db403.ping(True)   #实现超时自动连接
#password = os.getenv("NEO4J_PASSWORD")
#driver = GraphDatabase.driver('bolt://localhost',auth=basic_auth("neo4j", password))
# curs = db403.cursor()
# query = "SELECT * FROM enterprise_copy where name = %s"
# param = ("戚石飞",)
# curs.execute(query, param)
# # curs.execute("SELECT * FROM enterprise where id = %s", ("00000029-019c-4c91-86dd-3c20c946d09d",))
# # #curs.execute("SELECT * FROM enterprise where id = '00000029-019c-4c91-86dd-3c20c946d09d'")
# rv = curs.fetchall()
# ids = None
# for t in rv:
#     if t:
#         ids = t[1]
#     else:
#         ids = None
# print(ids)
# name = rv[0][0]
# name = [name]
# print(name)
#driver = GraphDatabase.driver("bolt://10.168.7.245:7687", auth=("neo4j", "123456"))
db = Graph("bolt://localhost:7687",password="123456")
# def get_db():
#     if not hasattr(g, 'neo4j_db'):
#         g.neo4j_db = driver.session()
#     return g.neo4j_db
#
# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'neo4j_db'):
#         g.neo4j_db.close()

@app.route("/")
def get_index():
    #return app.send_static_file('index.html')
    return "he"


def serialize_company(m):
    return {
        'id': m['id'],
        'name': m['name'],
        'stockId': m['stockId'],
    }
def serialize_papers(m):
    return {
        'paperID': m[0],
        'URI': m[1],
        'Title': m[2],
        'Abstract': m[3],
        'Year': m[4],
        'Conference': m[5],
        'Publish': m[6],
    }
def serialize_company(m):
    return {
        'id': m[0],
        'name': m[1],
        'status': m[2],
        'oper_name': m[3],
        'start_date': m[4],
        'reg_no': m[5],
        'reg_capi_desc': m[6],
        'org_no': m[7],
        'credit_no': m[8],
        'domains': m[9],
        'partners': m[10],
        'phones': m[11],
        'emails': m[12],
        'addresses': m[13],
        'websites': m[14],
        'faxs': m[15],
        'staffs': m[16],
        'permission': m[17],
        'scope': m[18],
        'econ_kind': m[19],
        'province': m[20],
        'category': m[21],
        'parent_domains': m[22],
        'belong_org': m[23],
        'reg_address': m[24],
    }
# def serialize_cast(cast):
#     return {
#         'name': cast[0],
#         'job': cast[1],
#         'role': cast[2]
#     }

@app.route("/mysql")
def get_items():
    curs = dbs.cursor()
    try:
        curs.execute("SELECT * FROM papers")
        rv = curs.fetchall()
    except:
        print ("Error: unable to fetch items")
    return Response(dumps([serialize_papers(record) for record in rv]),
                    mimetype="application/json")
@app.route("/mysql/search")
def mysql_search():
    curs = dbs.cursor()
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        query = "SELECT * FROM papers where PaperID = %s"
        param = q
        curs.execute(query, param)
        rv = curs.fetchall()
    return Response(dumps([serialize_papers(i) for i in rv]),
                    mimetype="application/json")
@app.route("/enterpriseid", methods=['GET'])
def enterprise_search():
    curs = db403.cursor()
    try:
        id = request.args["id"]
    except KeyError:
        return dumps({"statuscode":401,"statusmsg":"query parameter error!"})
    else:
        query = "SELECT * FROM enterprise_copy1 where credit_no = %s"  #enterprise_copy1 credit_no
        param = (id,)
        curs.execute(query, param)
        rv = curs.fetchall()
        ids = None
        for t in rv:
            if t:
                ids = t[0]     #t[0]
                #print(ids)
            else:
                ids = None
        query2 = "SELECT * FROM enterprise where id = %s"
        param2 = (ids,)
        curs.execute(query2, param2)
        rv2 = curs.fetchall()
        #print(len(rv2))
        if len(rv2) == 0:
            return dumps({"statuscode": 404, "statusmsg": "query no result!"})
        else:
            return dumps({"statuscode": 0, "statusmsg": "success", "result": [serialize_company(i) for i in rv2]},ensure_ascii=False)


    #return Response(dumps([serialize_company(i) for i in rv]),
                    #mimetype="application/json")
                #return dumps({"statuscode": 404, "statusmsg": "query no result!"})

@app.route("/enterprisename", methods=['GET'])
def enterprise_search1():
    curs = db403.cursor()
    try:
        name = request.args["name"]
    except KeyError:
        return dumps({"statuscode":401,"statusmsg":"query parameter error!"})
    else:
        query = "SELECT * FROM enterprise_copy where name = %s"  #enterprise_copy1 credit_no
        param = (name,)
        curs.execute(query, param)
        rv = curs.fetchall()
        ids = None
        for t in rv:
            if t:
                ids = t[1]
                #print(ids)
            else:
                ids = None
        query2 = "SELECT * FROM enterprise where id = %s"
        param2 = (ids,)
        curs.execute(query2, param2)
        rv2 = curs.fetchall()
        #print(len(rv2))
        if len(rv2) == 0:
            return dumps({"statuscode": 404, "statusmsg": "query no result!"})
        else:
            return dumps({"statuscode": 0, "statusmsg": "success", "result": [serialize_company(i) for i in rv2]},ensure_ascii=False)

dep = 0   #修改全局变量
@app.route("/holdername")
def holder_search():
    try:
        global dep
        name= request.args["name"]
        dep = request.args["depth"]
    except KeyError:
        return dumps({"statuscode": 401, "statusmsg": "query parameter error!"})
    else:
        name = [name]  #字符串变成数组
        depth = int(dep)  #字符串变成整型
        #print(type(name))
        a = combine(name,depth)
        b = combine1(name,depth)
        if len(b) == 0:                  #len(a)不行？？？
            return dumps({"statuscode": 404, "statusmsg": "query no result!"})
        else:
            return dumps({"statuscode": 0, "statusmsg": "success", "data": a,"links":b}, ensure_ascii=False)

    #return Response(dumps(a),mimetype="application/json")

des = 0
@app.route("/holderid")
def holder_search2():
     curs = db403.cursor()
     try:
         global des  #全局变量随depth变化
         id = request.args["id"]
         des = request.args["depth"]
     except KeyError:
         return dumps({"statuscode": 401, "statusmsg": "query parameter error!"})
     else:
         query = "SELECT * FROM enterprise_copy1 where credit_no = %s"  #enterprise_copy1  credit_no
         param = (id,)
         curs.execute(query, param)
         rv1 = curs.fetchall()
         if len(rv1) == 0:
             return dumps({"statuscode": 404, "statusmsg": "query no result!"})
         ids = None
         for t in rv1:
             if t:
                 ids = t[0]
                 # print(ids)
             else:
                 ids = None
         query2 = "SELECT * FROM enterprise where id = %s"
         param2 = (ids,)
         curs.execute(query2, param2)
         rv2 = curs.fetchall()
         name = rv2[0][1]
         name = [name]  #字符串变成数组
         depth = int(des)  #字符串变成整型
         #print(type(name))
         a = combine5(name,depth)
         b = combine1(name, depth)
         return dumps({"statuscode": 0, "statusmsg": "success", "result": a,"links":b}, ensure_ascii=False)
     #return Response(dumps(a),mimetype="application/json")
     #return dumps({"statuscode":0,"statusmsg":"success","result":a}, ensure_ascii=False)

@app.route("/graph")
def get_graph():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        results = db.run("MATCH (m:Stock)<-[r:CONTAINS]-(a) "
                     "WHERE m.name ={name} "
                     "RETURN m.name as holder, collect(a.name) as company ", {"name": q })
        #print(results)
        nodes = []
        rels = []
        i = 0
        for record in results:
            nodes.append({"name": record["holder"], "label": "holder"})
            target = i
            i += 1
            for name in record['company']:
                company = {"name": name, "label": "company"}
                try:
                    source = nodes.index(company)
                except ValueError:
                    nodes.append(company)
                    source = i
                    i += 1
                rels.append({"source": name, "target": record["holder"],"label": "CONTAINS"})
        return Response(dumps({"nodes": nodes, "links": rels}),
                        mimetype="application/json")

@app.route("/search")
def get_search():
    try:
        q = request.args["q"]
    except KeyError:
        return []
    else:
        #db = get_db()
        results = db.run("MATCH (m:Stock) "
                 "WHERE m.name =~ {name} "
                 "RETURN m", {"name": "(?i).*" + q + ".*"}
        )
        return Response(dumps([serialize_company(record['m']) for record in results]),
                        mimetype="application/json")
@app.route("/level")
def get_level():
    data = db.run("MATCH path=(n1{name:'山东省企业托管经营股份有限公司'})<-[*1..2]-(n2) RETURN path" ).data()
    nodes_source = []
    nodes_target = []
    rels = []
    for record in data:
        pathIdx = 0
        # print(record)
        for path in record['path']:
            # print(path)
            source = path.start_node['name']
            target = path.end_node['name']
            nodes_source.append({"name": source, "category": pathIdx + 1})
            nodes_target.append({"name": target, "category": pathIdx})
            pathIdx += 1
            node = nodes_source + nodes_target
            rels.append({"source": source, "target": target, "label": path['STOCK_PERCENT']})
    #点去重
    temp = []
    [temp.append(i) for i in node if not i in temp]
    return Response(dumps({"nodes": temp, "links": rels}),
                        mimetype="application/json")
@app.route("/level_search")
def get_levelsearch():
    try:
        q = request.args["q"]
        p = request.args["p"]
    except KeyError:
        return []
    else:
        #db = get_db()
        results = db.run("MATCH path = (n1:Stock)<-[r:*1..{p}]-(n2) WHERE n1.name={name} RETURN path",{"name":q,"level":p }).data()
        #db.run("MATCH path=(n1{name:'山东省企业托管经营股份有限公司'})<-[*1..2]-(n2) RETURN path").data()
        #print(results)
        nodes_source = []
        nodes_target = []
        rels = []
        for record in results:
            pathIdx = 0
            # print(record)
            for path in record['path']:
                # print(path)
                source = path.start_node['name']
                target = path.end_node['name']
                nodes_source.append({"name": source, "category": pathIdx + 1})
                nodes_target.append({"name": target, "category": pathIdx})
                pathIdx += 1
                node = nodes_source + nodes_target
                rels.append({"source": source, "target": target, "label": path['STOCK_PERCENT']})
        # 点去重
        temp = []
        [temp.append(i) for i in node if not i in temp]
        return Response(dumps({"nodes": temp, "links": rels}),
                        mimetype="application/json")

@app.route("/movie/<title>")
def get_movie(title):
    #db = get_db()
    results = db.run("MATCH (movie:Movie {title:{title}}) "
             "OPTIONAL MATCH (movie)<-[r]-(person:Person) "
             "RETURN movie.title as title,"
             "collect([person.name, "
             "         head(split(lower(type(r)), '_')), r.roles]) as cast "
             "LIMIT 1", {"title": title})

    result = results.single();
    return Response(dumps({"title": result['title'],
                           "cast": [serialize_cast(member)
                                    for member in result['cast']]}),
                    mimetype="application/json")


# if __name__ == '__main__':
#     app.run(port=8080)


