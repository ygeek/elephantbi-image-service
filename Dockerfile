FROM python:3.6.3

RUN apt-get update && \
    apt-get install -y \
    nginx \
	supervisor \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    lsb-release \
    xdg-utils \
    libgconf-2-4 \
    fonts-arphic-ukai \
    fontconfig \
    xfonts-utils

# Install Chrome for Selenium
COPY ./config/files/chrome.deb /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

# Install chromedriver for Selenium
COPY ./config/files/chromedriver /usr/local/bin/chromedriver
RUN chmod +x /usr/local/bin/chromedriver

RUN rm -rf /var/lib/apt/lists/*

# setup nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY config/deploy/nginx.conf /etc/nginx/sites-available/default

# setup supervisor to run nginx and uwsgi
COPY config/deploy/supervisord.d/* /etc/supervisord.d/
COPY config/deploy/supervisord.conf /etc/supervisord.conf

# set up fonts
RUN mkdir -p /usr/share/fonts/local && \
    chmod -R 777 /usr/share/fonts/local
COPY ./config/files/msyh.ttf /usr/share/fonts/local/msyh.ttf
RUN cd /usr/share/fonts/local && \
    mkfontscale && \
    mkfontdir && \
    fc-cache -fv

# COPY requirements.txt and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY ebi_image_service/requirements.txt /home/docker/code/
RUN pip install --upgrade pip
RUN pip install -Ur /home/docker/code/requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com

EXPOSE 80

COPY . /home/docker/code/

WORKDIR /home/docker/code/

ENV PATH="/home/docker/bin:${PATH}"

COPY config/deploy/start.py /home/docker/bin/entrypoint
RUN chmod a+x /home/docker/bin/entrypoint && mkdir -p /var/logs/
ENTRYPOINT ["entrypoint"]
