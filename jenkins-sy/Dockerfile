# VERSION 0.0.1
# This is a dockerfile for jenkins-api
# run a http server at port 8999
# require a jenkins application to support our server

FROM centos:latest

MAINTAINER captain "captain@cmaster.co"

RUN yum update -y & yum install -y wget python-devel
RUN wget -P ~/ https://bootstrap.pypa.io/get-pip.py --no-check-certificate
RUN python ~/get-pip.py
RUN pip install jinja2 requests python-jenkins jenkinsapi bottle
RUN pip install gevent
RUN echo https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.1.3.tar.gz >> requirements.txt
RUN pip install -r ./requirements.txt
RUN yum install -y gcc gcc-c++
RUN yum install -y glibc-static
RUN pip install uwsgi
RUN pip install dumb-init

ADD ./uwsgi.yml /etc/uwsgi.yml
ADD ./jenkins-sy /opt/jenkins-sy

ENV JENKINS_ADDRESS http://10.254.9.56:9000
ENV JENKINS_USER admin
ENV JENKINS_PASS 123456
ENV DB_HOST 10.254.9.56
ENV DB_PORT 3306
ENV DB_USER root
ENV DB_PASS my-secret-pw
ENV DB_NAME jenkins

ENTRYPOINT ["dumb-init"]
CMD ["/usr/bin/uwsgi", "--yml", "/etc/uwsgi.yml"]