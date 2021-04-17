FROM python:3.7-alpine

ENV LANG C.UTF-8
ENV TZ=Asia/Seoul

# Copy data for add-on
COPY run.sh /
COPY ezvill2mqtt /ezvill2mqtt

# Install requirements for add-on
RUN python3 -m pip install paho-mqtt

WORKDIR /share

RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
