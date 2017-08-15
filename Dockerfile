FROM python
MAINTAINER Jason Walsh <jason.walsh@uphs.upenn.edu>
COPY . /tmp
WORKDIR /tmp
RUN python setup.py install
ENTRYPOINT [ "mantis" ]
