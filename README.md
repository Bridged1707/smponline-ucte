# smponline-ucte

sudo puppet agent -t --server puppet

sudo systemctl status github-runner

sudo systemctl status smponline-ucte.service

sudo puppet agent -t --server puppet

TEST

# Service
```
administrator@prod-ucte-r001:~$ cat /etc/systemd/system/ucte.service
[Unit]
Description=UCTE Market Ingest Service
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=administrator
WorkingDirectory=/git/smponline-ucte
Environment=PYTHONUNBUFFERED=1
ExecStart=/bin/bash -lc 'mkdir -p logs && LOGFILE="logs/ucte_$(date +%%Y-%%m-%%d_%%H-%%M-%%S).log" && exec /usr/bin/python3 -m ucte.main >> "$LOGFILE"
2>&1'
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```
