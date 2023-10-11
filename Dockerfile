FROM python:3.9.9-slim-buster

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc wget python3-pip

ENV PYTHON_TA_LIB_PACKAGE_NAME "TA-lib"
ENV PYTHON_TA_LIB_VERSION "0.4.23"

RUN mkdir bassie && \
    cd bassie && \
    wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib/ && \
    ./configure --prefix=/usr && \
    make && \
    make install

RUN pip3 install ${PYTHON_TA_LIB_PACKAGE_NAME}==${PYTHON_TA_LIB_VERSION}

COPY ./crypto-python .

RUN pip3 install -r requirements.txt
 
ENTRYPOINT ["python3"]
CMD ["main.py"]