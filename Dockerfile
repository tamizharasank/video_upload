FROM ubuntu:16.04

MAINTAINER cognativeAR
WORKDIR /index
COPY . /index
ENTRYPOINT [ "python" ]
CMD [ "index.py" ]