# install dependencies
pip3 install -r requirements.txt

# SECRET_KEY
python3 -c "import secrets; print(secrets.token_hex(32))"

# PASSWORD_HASH
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('мой_пароль'))"

# make log dir
mkdir -p /var/log/achievement_tracker

# systemd service file symlink
ln -s /root/myfirstvps/web_services/systemd.conf /etc/systemd/system/achievement_tracker.service
systemctl daemon-reload
systemctl enable --now achievement_tracker.servic

# nginx config file symlink
ln -s /root/myfirstvps/web_services/nginx.conf /etc/nginx/sites-enabled/achievement_tracker
nginx -t
systemctl restart nginx