FROM node:10-alpine
# Install Python.
# RUN \
#   apt-get update && \
#   apt-get install -y python3 python3-dev python-pip python-virtualenv && \
#   pip3 install --upgrade pip setuptools && \
#   rm -rf /var/lib/apt/lists/*
RUN apk update && apk upgrade \
    && apk add tini curl python python-dev python3 python3-dev py-setuptools sudo \
    linux-headers build-base bash git ca-certificates && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    rm -r /root/.cache \
## Dev dependencies and others stuffs...
    && echo "|--> Install build dependencies" \
    && apk add -U --virtual=.build-deps \
        build-base linux-headers python3-dev git cmake jpeg-dev \
        libffi-dev openblas-dev py-numpy-dev freetype-dev libpng-dev \
    && echo "|--> Install Python packages" \
    && pip install -U pillow zmq \
# Install PyTorch
    && echo "|--> Clone PyTorch" \
    && git clone --recursive https://github.com/pytorch/pytorch \
    && echo "|--> Install PyTorch" \
    && cd pytorch && python setup.py install \
    && echo "|--> Clone Torch Vision" \
    && git clone --recursive https://github.com/pytorch/vision \
    && echo "|--> Install Torch Vision" \
    && cd vision && python setup.py install \
## Cleaning
    && echo "|--> Cleaning" \
    && rm -rf /pytorch \
    && rm -rf /root/.cache \
    && find /usr/lib/python3.6 -name __pycache__ | xargs rm -r \
    && rm -rf /root/.[acpw]* \
    && rm /usr/include/xlocale.h \
    && rm -rf /var/cache/apk/* \
    && apk del .build-deps
    
# Create working directory
WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 8888

CMD ["npm", "start"]