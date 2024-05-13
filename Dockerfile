FROM python:3.12-alpine
ENV TZ=Asia/Bangkok

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt && crontab /app/crontab

ENTRYPOINT ["/usr/sbin/crond", "-f", "-d", "5"]
