from continuumio/anaconda3:5.3.0

run apt-get update && apt-get install -y g++ openjdk-8-jdk

run pip install -qq konlpy ujson pyecharts

run useradd -d /app -m -s /bin/bash beomi && echo "beomi:beomi" | chpasswd && adduser beomi sudo

run chown -R beomi:beomi /app

workdir /app

copy jupyter_notebook_config.json /app 

expose 18888 

cmd ["jupyter-notebook", "--ip=0.0.0.0", "--port=18888", "--allow-root"]

