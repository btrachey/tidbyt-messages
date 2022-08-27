FROM arm64v8/ubuntu

ENV PIXLET_VERSION 0.18.1
ENV PIXLET_FILENAME pixlet_${PIXLET_VERSION}_linux_amd64.tar.gz
ENV PIXLET_URL https://github.com/tidbyt/pixlet/releases/download/v${PIXLET_VERSION}/${PIXLET_FILENAME}

RUN apt-get update && \
    apt-get install -y -- \
      ca-certificates \
      python3 \
      python3-pip \
      curl \
      tar \
      gzip

RUN curl -L "$PIXLET_URL" -o /usr/local/bin/$PIXLET_FILENAME && \
    tar -xf /usr/local/bin/$PIXLET_FILENAME -C /usr/local/bin

RUN python3 -m pip install awslambdaric

COPY app.py .
COPY text.star .

ADD https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie /usr/bin/aws-lambda-rie
COPY entry.sh /
RUN chmod 755 /usr/bin/aws-lambda-rie /entry.sh
ENTRYPOINT [ "/entry.sh" ]
CMD [ "app.handler" ]
