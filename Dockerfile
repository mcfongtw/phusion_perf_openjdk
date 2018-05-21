# ubuntu-perf-openjdk-8
#
#
# Extends ubuntu-perf-base with java 8 openjdk jdk installation
#
# TODO : Move to another repo and rebuild docker build automation
#
#
FROM mcfongtw/ubuntu_perf_tools:16.04

MAINTAINER Michael Fong <mcfong.open@gmail.com>

####################################################### 
# Use baseimage-docker's init system.
CMD ["/sbin/my_init"]

WORKDIR /workspace

RUN apt-get update
####################################################### 
# This is in accordance to : https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04
RUN apt-get install -y openjdk-8-jdk && \
	apt-get install -y ant && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk8-installer;
	
####################################################### 
# Fix certificate issues, found as of 
# https://bugs.launchpad.net/ubuntu/+source/ca-certificates-java/+bug/983302
RUN apt-get update && \
	apt-get install -y ca-certificates-java && \
	apt-get clean && \
	update-ca-certificates -f && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk8-installer;

####################################################### 
# debug symbol for openjdk
RUN apt-get update && \
        apt-get install -y openjdk-8-dbg && \
	apt-get clean && \
	rm -rf /var/lib/apt/lists/* && \
	rm -rf /var/cache/oracle-jdk8-installer;

####################################################### 
# Setup JAVA_HOME, this is useful for docker commandline
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN export JAVA_HOME

####################################################### 
# Compile perf-map-agent from source code
RUN git clone --depth=1 https://github.com/jvm-profiling-tools/perf-map-agent.git /workspace/perf-map-agent

# Install build required dependencies
RUN apt-get update && \
        apt-get install -y g++ && \
	apt-get clean; 

RUN cd /workspace/perf-map-agent/ && \
	cmake . && \
	make ;

####################################################### 
# Setup entry point
COPY docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

####################################################### 
# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
