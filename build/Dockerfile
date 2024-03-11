# ベースイメージ
FROM ubuntu:22.04

# Set proxy
ARG http_proxy=""
ARG https_proxy=""
ENV HTTP_PROXY=${http_proxy} \
    HTTPS_PROXY=${https_proxy} \
    http_proxy=${http_proxy} \
    https_proxy=${https_proxy}
RUN sh -c 'echo Acquire::http::proxy \"${http_proxy}\"\;' >> /etc/apt/apt.conf
RUN sh -c 'echo Acquire::https::proxy \"${https_proxy}\"\;' >> /etc/apt/apt.conf

# 日本語表示用環境設定
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# aptモジュールインストール
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3.10
RUN apt-get install -y python3-pip
RUN apt-get install -y less vim sudo wget curl git
RUN apt-get install -y python-is-python3
RUN apt-get install -y libgl1-mesa-dev
RUN apt-get install -y libglib2.0-0

# 環境変数を設定

# https://www.lifewithpython.com/2021/05/python-docker-env-vars.html
# 非空なら .pyc を生成しない
ENV PYTHONDONTWRITEBYTECODE 1
# 非空なら標準出力・標準エラーのストリームのバッファリングを行わない
ENV PYTHONUNBUFFERED 1

# パッケージインストール
RUN pip install --upgrade pip
RUN pip install numpy
RUN pip install openai==1.7.2
RUN pip install langchain==0.1.0
RUN pip install langchain_openai==0.0.2.post1
RUN pip install tiktoken
RUN pip install chromadb
RUN pip install faiss-cpu
RUN pip install streamlit
RUN pip install pypdf
RUN pip install clipboard
RUN pip install pyocr
RUN pip install pdf2image
RUN pip install opencv-python

# 環境変数設定
ENV PYTHONPATH "${PYTHONPATH}:/home/ubuntu/workspace/src"

## 権限定義 ##
ARG user_name=ubuntu
ARG user_id=1000
ARG group_name=ubuntu
ARG group_id=1000

RUN groupadd -g ${group_id} ${group_name}
RUN useradd -u ${user_id} -g ${group_id} -d /home/${user_name} --create-home --shell /usr/bin/bash ${user_name}
RUN echo "${user_name} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown -R ${user_name}:${group_name} /home/${user_name}

# ワークスペース定義
USER ubuntu
ENV HOME /home/ubuntu
WORKDIR /home/ubuntu/workspace