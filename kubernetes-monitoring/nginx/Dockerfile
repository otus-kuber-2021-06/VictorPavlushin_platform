FROM nginx:latest
COPY --chown=root:root nginx.conf /etc/nginx/nginx.conf
RUN chgrp -R root /var/cache/nginx /var/run /var/log/nginx && \
    chmod -R 770 /var/cache/nginx /var/run /var/log/nginx
EXPOSE 8000
USER 1001
