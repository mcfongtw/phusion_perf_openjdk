#
# Existing Tags:
# mcfongtw/phusion_perf_openjdk:latest
# mcfongtw/phusion_perf_openjdk:8
#
FROM mcfongtw/phusion_perf_platform:16.04

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
# SDKMan
RUN apt-get update && \
	apt-get install -y zip unzip;
RUN curl -s "https://get.sdkman.io" | bash
ENV SDKMAN_DIR /workspace/.sdkman
RUN set -x \
    && echo "sdkman_auto_answer=true" > $SDKMAN_DIR/etc/config \
    && echo "sdkman_auto_selfupdate=false" >> $SDKMAN_DIR/etc/config \
    && echo "sdkman_insecure_ssl=false" >> $SDKMAN_DIR/etc/config
####################################################### 
# Maven
RUN /bin/bash -c " source $SDKMAN_DIR/bin/sdkman-init.sh && sdk install maven"

####################################################### 
#FIXME: The perf installation did not propagated properly from upstream. Remove this once resolved.
#
# perf related
#
RUN apt-get update && \ 
	apt-get install -y linux-tools-common linux-tools-generic linux-tools-`uname -r`
#
# Set permission to collect perf stat
# -1 - Not paranoid at all
RUN echo 'kernel.perf_event_paranoid = -1' > /etc/sysctl.d/perf.conf
####################################################### 
# Compile perf-map-agent from source code
RUN git clone --depth=1 https://github.com/jvm-profiling-tools/perf-map-agent /workspace/perf-map-agent

# Install build required dependencies
RUN apt-get update && \
        apt-get install -y g++ && \
	apt-get clean; 

RUN cd /workspace/perf-map-agent/ && \
	cmake . && \
	make ;

####################################################### 
# Setup entry point
COPY docker-entrypoint.sh /workspace/docker-entrypoint.sh

RUN chmod +x /workspace/docker-entrypoint.sh

ENTRYPOINT ["/workspace/docker-entrypoint.sh"]

####################################################### 
# Copy perfJava
COPY perfJava /workspace/perfJava

####################################################### 
# Clean up APT when done.
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
