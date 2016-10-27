# VERSION 0.0.1
# This is a dockerfile for jenkins-api
# run a http server at port 8999
# require a jenkins application to support our server

FROM 192.168.1.11:5000/ddcos-sagent:v0.0.67

MAINTAINER captain "captain@cmaster.co"

#RUN yum install -y deb
RUN pip install jinja2 requests python-jenkins jenkinsapi bottle mysql-connector-python

ADD ./uwsgi.yml /etc/uwsgi.yml
ADD ./jenkins-sy /opt/jenkins-sy

ENV JENKINS_ADDRESS http://127.0.0.1:9000
ENV JENKINS_USER admin
ENV JENKINS_PASS admin
ENV DB_HOST 127.0.0.1
ENV DB_PORT 3366
ENV DB_USER root
ENV DB_PASS root
ENV DB_fNAME jenkins

ENTRYPOINT ["dumb-init"]
CMD ["/usr/sbin/uwsgi", "--yml", "/etc/uwsgi.yml"]