#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Jack

import CIJenkins
import json
from bottle import Bottle, request, response
import dbclient

app = Bottle()

@app.route('/createJob', method='POST')
def createJob():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')
	conf = data.get('conf')
	try:
		dbclient.addRecords(conf)
	except Exception, e:
		return {'st':'error','data':str(e)}

	xml = jenkins.generateXml(conf)
	return {'st': jenkins.addJob(appid, xml)}


@app.route('/getRegistry', method='POST')
def getRegistry():
	data = json.loads(request.body.read())
	userid = data.get('userid')
	
	try:
		registry = dbclient.getRegistry(userid)
	except Exception, e:
		return {'st':'error','data':str(e)}

	return {'registry':registry}


@app.route('/buildJob', method='POST')
def buildJob():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')
	userid = data.get('userid')
	repo = data.get('repo')
	url = data.get('url')

	avg = {}
	avg['USERNAME'],avg['PASSWORD'],avg['REGISTRY'],avg['REPO'] = dbclient.getUP(userid,url,repo)

	st = jenkins.buildJob(appid, avg)

	return {'st': st}


@app.route('/updateJob', method='POST')
def updateJob():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')
	conf = data.get('conf')
	try:
		dbclient.updateRecords(conf)
	except Exception, e:
		return {'st':'error','data':str(e)}

	xml = jenkins.generateXml(conf)
	return {'st': jenkins.updateJob(appid, xml)}


@app.route('/deleteJob', method='POST')
def deleteJob():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')
	try:
		st = jenkins.deleteJob(appid)
		dbclient.delRecords(appid)
	except Exception, e:
		return {'st':'error','data':str(e)}
	return {'st': 'ok'}


@app.route('/getJob', method='POST')
def getJob():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')

	return jenkins.queryJob(appid)


@app.route('/listJob', method='POST')
def listJob():
	data = json.loads(request.body.read())
	appid = data.get('appid')

	jobs = dbclient.getJobs(appid)

	return {'jobs':jobs}


@app.route('/runCheck', method='POST')
def runCheck():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')

	r_data = jenkins.runCheck(appid)
	r_data['lastStatus'] = jenkins.getbuildStatus(appid)
	r_data['lastSucceed_time'], r_data['lastSucceed_num'] = jenkins.getLastSucceed(appid)
	r_data['lastFail_time'], r_data['lastFail_num'] = jenkins.getLastFail(appid)

	return r_data


@app.route('/buildConsole', method='POST')
def buildConsole():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')
	number = data.get('buildid')

	return jenkins.getbuildconsole(appid,number)


@app.route('/buildList', method='POST')
def buildList():
	jenkins = CIJenkins.CIJenkins()

	data = json.loads(request.body.read())
	appid = data.get('appid')

	return jenkins.getbuildids(appid)


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=9999)