FROM nginx:1.27.5-alpine


WORKDIR /app


COPY ./static /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/nginx.conf

EXPOSE 8080
