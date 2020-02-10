FROM node:lts
RUN mkdir /source_code
ADD ./code /source_code/
WORKDIR /source_code
RUN npm install
RUN npm install pm2 -g