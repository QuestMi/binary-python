FROM ubuntu:18.04

RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN  sed -i s@/security.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

ENV IGNORE_FILES = [], PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple/
RUN apt-get update -y && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends  \
    && python3 python3-pip python3-dev python3-venv \
    && rm /bin/sh && ln -s /bin/bash /bin/sh \
    && rm -rf /var/lib/apt/lists/*
    # && python3.8 python3-pip python3.8-dev python3.8-venv \
    # && ln -s /usr/bin/python3.8 /usr/bin/python3 \

RUN mkdir -p /opt/apps/
WORKDIR /opt/apps/
COPY ../requirements.txt ./requirements.txt
RUN python3 -m venv python \
    && source python/bin/activate \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r ./requirements.txt
RUN chmod a+x start.sh
ENTRYPOINT [ "./start.sh" ]