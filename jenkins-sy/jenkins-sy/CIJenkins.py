#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Jack

import json
import mysql.connector
import requests
import jenkins
from jenkinsapi.jenkins import Jenkins
#import dbclient
import jinja2
import uuid
from setting import *
import time


class CIJenkins(object):
	"""docstring for CIJenkins"""
	def __init__(self):
		super(CIJenkins, self).__init__()
		self.server = jenkins.Jenkins(jenkins_address,username=jenkins_username,password=jenkins_password)
		self.server_status = Jenkins(jenkins_address,username=jenkins_username,password=jenkins_password)

	FILE_PATH = "~/"

	def generateXml(self, conf):
		templateLoader = jinja2.FileSystemLoader(searchpath='./template/')
		templateEnv = jinja2.Environment(loader=templateLoader)
		TEMPLATE_FILE = '%s-conf.xml.j2'

		templateVars = {
				"appid": conf['appid'],
				"description": conf['description'] if conf.has_key('description') else "",
				"address": conf['address'],
				"branch": conf['branch'] if conf['branch'] != "" else "master",
				"tag": conf['tag']
		}
		temp_type = conf['type'].lower()
		templateVars['avg'] = ['USERNAME','PASSWORD','REGISTRY','REPO']
		if conf.has_key('username') and conf['username'] != "":
			cd = {'username':conf['username'],'password':conf['password'],'desc': conf['appid']}
			userid = self.createCredentials(cd)
			if userid != "":
				templateVars['userid'] = userid

		TEMPLATE_FILE = TEMPLATE_FILE % temp_type
		template = templateEnv.get_template(TEMPLATE_FILE)
		outputText = template.render(templateVars)

		return outputText

	def addJob(self, name, xml):
		try:
			self.server.create_job(name, xml)
			return "ok"
		except Exception,e:
			return "error: %s"%str(e)

	def buildJob(self, name, avg=None):
		try:
			num = self.server_status[name].get_next_build_number()
			if avg is None:
				self.server.build_job(name)
			else:
				self.server.build_job(name,avg)
			return "ok", num
		except Exception,e:
			return "error: %s"%str(e)

	def updateJob(self, name, xml):
		try:
			self.server.reconfig_job(name, xml)
			return "ok"
		except Exception, e:
			return "error: %s"%str(e)

	def deleteJob(self, name):
		try:
			self.server.delete_job(name)
			return "ok"
		except  Exception as e:
			return "error: %s " % str(e)

	def queryJob(self, name):
		r_data = {}
		try:
			build_info = self.server.get_job_info(name)
			r_data['data'] = build_info
			r_data['st'] = 'ok'
		except Exception,e:
			r_data['st'] = 'error: %s'%str(e)
		finally:
			return r_data

	def listJob(self):
		r_data = {}
		try:
			jobs = self.server.get_jobs()
			r_data['data'] = jobs
			r_data['st'] = 'ok'
		except Exception,e:
			r_data['st'] = 'error: %s'%str(e)
		finally:
			return r_data

	def runCheck(self, name):
		r_data = {}
		try:
			job = self.server_status[name]
			r_data['running'] = job.is_running()
			r_data['queued'] = job.is_queued()
			r_data['st'] = 'ok'
		except Exception,e:
			r_data['st'] = 'error: %s'%str(e)
		finally:
			return r_data

	def createCredentials(self, cd):
		try:
			cd_id = uuid.uuid1()
			cd_username = cd['username']
			cd_password = cd['password']
			cd_desc = cd['desc']

			s = requests.Session()
			get_first_cookie = s.get(jenkins_address)
			get_login_jc = s.get(jenkins_address+"/login?from=/")
			jc = get_login_jc.content
			begin = int(jc.find('crumb.init("Jenkins-Crumb"'))
			jc = jc[begin+29:begin+29+32]
			login_data = u'''j_username={j_username}&j_password={j_password}&from=%2F\
			&json=%7B%22j_username%22%3A+%22{j_username}%22%2C+%22j_password%22%3A+%22{j_password}%22%2C+%22remember_me%22%3A+false%2C+%22from%22%3A+%22%2F%22%2C+%22Jenkins-Crumb%22%3A+%22{jc}%22%7D\
			&Submit=%E7%99%BB%E5%BD%95'''.format(j_username=jenkins_username, j_password=jenkins_password, jc=jc)
			lg_headers = {
				"Origin": "{}".format(jenkins_address),
				"Upgrade-Insecure-Requests": "1",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
				"Content-Type": "application/x-www-form-urlencoded",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Referer": "{}/login?from=%2F".format(jenkins_address),
				"Accept-Encoding": "gzip, deflate",
				"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
			}
			login = s.post(jenkins_address+"/j_acegi_security_check", data=login_data, headers=lg_headers, allow_redirects=True)
			gc_header = {
				"Host": "{}".format(jenkins_address[7:]),
				"Upgrade-Insecure-Requests": "1",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Referer": "{}/credentials/store/system/domain/_/".format(jenkins_address),
				"Accept-Encoding": "gzip, deflate, sdch",
				"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
			}
			get_credentials_jc = s.get(jenkins_address+"/credentials/store/system/domain/_/newCredentials",headers=gc_header)
			jc = get_credentials_jc.content

			begin = int(jc.find('crumb.init("Jenkins-Crumb"'))
			jc = jc[begin+29:begin+29+32]
			credentials_data = '''_.scope=GLOBAL&_.username={user}&_.password={passwd}&_.id={id}&_.description={desc}\
&stapler-class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl\
&%24class=com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl\
&stapler-class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl\
&%24class=com.dabsquared.gitlabjenkins.connection.GitLabApiTokenImpl\
&stapler-class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey\
&%24class=com.cloudbees.jenkins.plugins.sshcredentials.impl.BasicSSHUserPrivateKey\
&stapler-class=org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl\
&%24class=org.jenkinsci.plugins.plaincredentials.impl.FileCredentialsImpl\
&stapler-class=org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\
&%24class=org.jenkinsci.plugins.plaincredentials.impl.StringCredentialsImpl\
&stapler-class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl\
&%24class=com.cloudbees.plugins.credentials.impl.CertificateCredentialsImpl\
&Jenkins-Crumb={jc}\
&json=%7B%22%22%3A+%220%22%2C+%22credentials%22%3A+%7B%22scope%22%3A+%22GLOBAL%22%2C+%22username%22%3A+%22{user}%22%2C+%22password%22%3A+%22{passwd}%22%2C+%22id%22%3A+%22{id}%22%2C+%22description%22%3A+%22{desc}%22%2C+%22stapler-class%22%3A+%22com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl%22%2C+%22%24class%22%3A+%22com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl%22%7D%2C+%22Jenkins-Crumb%22%3A+%22{jc}%22%7D\
&Submit=OK'''
			credentials_data = credentials_data.format(user=cd_username, passwd=cd_password, id=cd_id, desc=cd_desc, jc=jc)
			cd_headers = {
				"Origin": "{}".format(jenkins_address),
				"Upgrade-Insecure-Requests": "1",
				"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36",
				"Content-Type": "application/x-www-form-urlencoded",
				"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
				"Referer": "{}/credentials/store/system/domain/_/newCredentials".format(jenkins_address),
				"Accept-Encoding": "gzip, deflate",
				"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
			}
			add_credentials = s.post(jenkins_address+"/credentials/store/system/domain/_/createCredentials", data=credentials_data, headers=cd_headers)
		except :
			return ""
		else:
			return cd_id

	def getbuildStatus(self, name):
		try:
			build = self.getLastBuild(name)
			stat = build.get_status()
		except :
			stat = "None"
		return stat

	def getbuildconsole(self, name, number):
		r_data = {}
		try:
			build = self.server_status[name].get_build(number)
			r_data['st'] = 'ok'
			r_data['data'] = build.get_console().split("echo ''\n\n")
		except Exception,e:
			r_data['st'] = 'error: %s'%str(e)
		return r_data

	def getbuildids(self, name):
		job = self.server_status[name]
		build_ids = job.get_build_ids()
		ids = [i for i in build_ids]
		build_list = []
		for i in ids[:10]:
			build = job.get_build(i)
			time = build.get_timestamp()
			state = build.get_status()
			a = {'id':i,'time':str(time),'state':state}
			build_list.append(a)
		return {'ids':build_list}

	def getLastSucceed(self, name):
		try:
			job = self.server_status[name]
			num = job.get_last_good_buildnumber()
			time = job.get_build(num).get_timestamp()
		except Exception, e:
			time = ""
			num = 0

		return str(time), num

	def getLastFail(self, name):
		try:
			job = self.server_status[name]
			num = job.get_last_failed_buildnumber()
			time = job.get_build(num).get_timestamp()
		except Exception, e:
			time = ""
			num = 0

		return str(time), num

	def getLastBuild(self, name):
		try:
			stat = self.server_status[name].get_last_build()
		except Exception,e:
			stat = "None"
		return stat
