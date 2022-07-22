FROM python:3.7.6-buster

LABEL maintainer="sdiego@seidor.com.br"

ENV TZ=America/Sao_Paulo
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy the required files
COPY ./ /var/source

# SAP NetWeaver RFC SDK installation
ENV SAPNWRFC_HOME=/usr/local/sap/nwrfcsdk
ENV PATH="${SAPNWRFC_HOME}:${PATH}"
ENV LD_LIBRARY_PATH="${SAPNWRFC_HOME}/lib"

# Python requirements installation
RUN unzip /sap.zip -d /usr/local && rm -rf /sap.zip && mv nwrfcsdk.conf /etc/ld.so.conf.d && pip install --upgrade pip && pip install -r requirements.txt

# Workdir and Entrypoint
WORKDIR /var/source
# ENTRYPOINT /bin/sh
ENTRYPOINT python3 server.py
