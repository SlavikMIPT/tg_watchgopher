# tg_watchgopher
- Create Telegram private channel for backups
- Get channel id (@getidsbot)
- Edit main.py to include your own files to backup
- Edit dbbackup.service and dbbackup.timer and place to /etc/systemd/system
- sudo systemctl enable dbbackup.timer
- sudo systemctl daemon-reload
- sudo systemctl start dbbackup.timer
- sudo systemctl status dbbackup.timer