#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: Jack

import os

jenkins_address = os.environ.get("JENKINS_ADDRESS","http://127.0.0.1:9000")
jenkins_username = os.environ.get("JENKINS_USER","admin")
jenkins_password = os.environ.get("JENKINS_PASS","admin")


DB_USER = os.environ.get('DB_USER', 'root')
DB_PASS = os.environ.get('DB_PASS', 'root')
DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', '3366')
DB_NAME = os.environ.get('DB_NAME', 'captain')