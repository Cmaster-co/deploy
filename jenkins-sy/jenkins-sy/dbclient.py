#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Jack

import mysql.connector
from setting import *


config = {
    'user':DB_USER, 
    'password':DB_PASS, 
    'host':DB_HOST, 
    'port':DB_PORT,  
    'database':DB_NAME,
    'charset':'utf8'}

def getJobs(appid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        appid = "'%"+appid+"%'"
        sql = "SELECT appid,address,tag,branch,description,type FROM jenkins_cfg WHERE appid LIKE %s"%str(appid)
        cursor.execute(sql)
        j_list = []
        for appid,address,tag,branch,description,t in cursor:
            j_list.append({'appid':appid,'address':address,'tag':tag,'branch':branch,'description':description,'type':t})
    except mysql.connector.Error as e:
        print "Error: %s"%e
        return
    finally:
        cursor.close()
        conn.close()
    return j_list


def getUP(userid,url,repo):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        sql = "SELECT url,username,password FROM registry WHERE owner='%s' and url='%s' and repo='%s'"%(userid,url,repo)
        cursor.execute(sql)
        row = cursor.fetchone()
        Url = row[0]
        Username = row[1]
        Password = row[2]
    except mysql.connector.Error as e:
        print "Error: %s"%e
        return
    finally:
        cursor.close()
        conn.close()

    return Username,Password,Url

def getRegistry(userid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    r_list = []
    try:
        sql = "SELECT url,repo FROM registry WHERE owner='%s'"%str(userid)
        cursor.execute(sql)
        for url,repo in cursor:
            r_list.append({'url':url,'repo':repo})
    except mysql.connector.Error as e:
        print "Error: %s"%e
        return
    finally:
        cursor.close()
        conn.close()

    return r_list

def getSetting(appid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        sql = "SELECT appid,address,tag,branch,description,type FROM jenkins_cfg WHERE appid='%s' LIMIT 1"%str(appid)
        cursor.execute(sql)
        row = cursor.fetchone()
        conf['appid'] = row[0]
        conf['address'] = row[1]
        conf['tag'] = row[2]
        conf['branch'] = row[3]
        conf['description'] = row[4]
        conf['type'] = row[5]
    except mysql.connector.Error as e:
        print "Error: %s"%e
        return 
    finally:
        cursor.close()
        conn.close()

    return conf


def delRecords(appid):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM jenkins_cfg WHERE appid = '%s'"%str(appid)
        cursor.execute(sql)
        conn.commit()
    except  mysql.connector.Error as e:
        print "Error: %s"%e
    finally:
        cursor.close()
        conn.close()


def addRecords(cf):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO jenkins_cfg (appid,branch,address,type,description,tag)VALUES('%s','%s','%s','%s','%s','%s')"%(cf['appid'],cf['branch'],cf['address'],cf['type'],cf['description'],cf['tag'])
        cursor.execute(sql)
        conn.commit()
    except  mysql.connector.Error as e:
        print "Error: %s"%e
    finally:
        cursor.close()
        conn.close()


def updateRecords(cf):
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    try:
        sql = "UPDATE jenkins_cfg SET branch='%s',address='%s',type='%s',description='%s',tag='%s' WHERE appid='%s'"%(cf['branch'],cf['address'],cf['type'],cf['description'],cf['tag'],cf['appid'])
        cursor.execute(sql)
        conn.commit()
    except  mysql.connector.Error as e:
        print "Error: %s"%e
    finally:
        cursor.close()
        conn.close()