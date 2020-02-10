FROM ubuntu:18.04 as build

ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update -y && apt-get -qy install lsof \
ntp \
git \
python3 \
python3-dev \
python3-pip \ 
build-essential \
libssl-dev \
libjpeg-dev \
libpq-dev \
vim \
pkg-config \
libcairo2-dev \
# clean up apt cache to keep image size smaller
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

FROM build as repoClone

WORKDIR /root/.ssh
COPY id_rsa /root/.ssh/id_rsa
RUN chmod 700 /root/.ssh/id_rsa
RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config

WORKDIR /opt
RUN git clone --depth 1 git@github.com:fernando737/my2home.git

FROM repoClone as appBuild

WORKDIR /opt/my2home
COPY --from=repoClone /opt/my2home .
RUN pip3 install -r requirements.txt

FROM appBuild as entrypoint

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod ug+x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]
COPY nginx/nginx.conf /etc/my2home-nginx/
VOLUME ["/etc/my2home-nginx/"]