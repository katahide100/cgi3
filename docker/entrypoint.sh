#!/bin/bash
set -e

APP_DIR="/var/www/html/cgi3"
cd "$APP_DIR"

# Initialize cust.cgi from template if not exists
if [ ! -f cust.cgi ]; then
    cp cust.default.cgi cust.cgi
    echo "[entrypoint] Created cust.cgi from template"
fi

# Update hostname in cust.cgi
if [ -n "$HOST_NAME" ]; then
    sed -i "s|\$hostName.*=.*|\\\$hostName       = \"$HOST_NAME\";|" cust.cgi
    echo "[entrypoint] Set hostName = $HOST_NAME"
fi

# Set permissions
chmod 777 playerdata 2>/dev/null || true
chmod 777 room 2>/dev/null || true
chmod 777 logs 2>/dev/null || true
chmod 777 chat/data 2>/dev/null || true
chmod 777 data 2>/dev/null || true
chmod 777 taikai 2>/dev/null || true
chmod 777 tmp 2>/dev/null || true
chmod 777 lock 2>/dev/null || true

touch popular.dat 2>/dev/null && chmod 777 popular.dat 2>/dev/null || true
touch member.dat 2>/dev/null && chmod 777 member.dat 2>/dev/null || true
touch chat/data/data.log 2>/dev/null && chmod 777 chat/data/data.log 2>/dev/null || true
touch taikai/t_time.csv 2>/dev/null && chmod 777 taikai/t_time.csv 2>/dev/null || true
touch taikai/taikai.csv 2>/dev/null && chmod 777 taikai/taikai.csv 2>/dev/null || true

# Setup cron
echo "* * * * * $APP_DIR/roomreset.sh" > /tmp/crontab
echo "* * * * * $APP_DIR/script/permission_reset.sh" >> /tmp/crontab
echo "0 0 * * * $APP_DIR/script/logreset.sh" >> /tmp/crontab
echo "0 0 * * 0 $APP_DIR/script/populerreset.sh" >> /tmp/crontab
crontab /tmp/crontab
rm /tmp/crontab

cleanup() {
    echo "[entrypoint] Shutting down..."
    kill $NODE_PID 2>/dev/null || true
    exit 0
}
trap cleanup SIGTERM SIGINT

echo "[entrypoint] Starting cron..."
service cron start

echo "[entrypoint] Starting Node.js socket.io server..."
cd "$APP_DIR"
node app_node.js &
NODE_PID=$!

export PERL_UNICODE=SDAL
echo "[entrypoint] Starting Apache in foreground..."
apachectl -D FOREGROUND
