################################################
# Compile with:
#     docker build -t pythonbot -f Dockerfile .
#
# Run with:
#     docker run -d -p 5001:5001 pythonbot
#
#################################################

FROM python:3.8

# Install dependencies
RUN apt-get update && \
    apt-get install -y \
    locales locales-all \
    # git \
    # WebKit dependencies
    libwoff1 \
    libopus0 \
    libwebp6 \
    libwebpdemux2 \
    libenchant1c2a \
    libgudev-1.0-0 \
    libsecret-1-0 \
    libhyphen0 \
    libgdk-pixbuf2.0-0 \
    libegl1 \
    libxslt1.1 \
    libgles2 \
    # gstreamer and plugins to support video playback in WebKit
    libgstreamer-gl1.0-0 \
    libgstreamer-plugins-bad1.0-0 \
    gstreamer1.0-plugins-good \
    # Chromium dependencies
    libnss3 \
    libxss1 \
    libasound2 \
    fonts-noto-color-emoji \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxcomposite1 \
    libcups2 \
    libgtk-3-0 \
    # Firefox dependencies
    libdbus-glib-1-2 \
    libxt6 \
    # FFmpeg to bring in audio and video codecs necessary for playing videos in Firefox
    ffmpeg \
    # (Optional) XVFB if there's a need to run browsers in headful mode
    xvfb \
    # For compiling libjpeg for WebKit
    curl \
    gcc \
    make

# Compiling libjpeg for WebKit
RUN cd /tmp && \
    curl -s http://www.ijg.org/files/jpegsrc.v8d.tar.gz | tar zx && \
    cd jpeg-8d && \
    ./configure && \
    make && \
    make install

# Add directory in which libjpeg was built to the search path
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH


# Add user so we don't need --no-sandbox in Chromium
# RUN groupadd -r pwuser && useradd -r -g pwuser -G audio,video pwuser \
#     && mkdir -p /home/pwuser/Downloads \
#     && chown -R pwuser:pwuser /home/pwuser

# # Run everything after as non-privileged user
# USER pwuser

RUN pip install --upgrade pip

COPY . /var/www/app
RUN pip install -r /var/www/app/requirements.txt
RUN python -m playwright install

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

CMD [ "python", "./var/www/app/main.py" ]
