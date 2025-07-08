FROM nginx:alpine

COPY nginx.conf /etc/nginx/nginx.conf
COPY globe /usr/share/nginx/html/globe
COPY globe/index.html /usr/share/nginx/html/index.html


# COPY nginx.conf /etc/nginx/conf.d/default.conf
# COPY globe /usr/share/nginx/html/globe
