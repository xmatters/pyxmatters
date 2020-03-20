environment = {
    "url": "https://<instance>.xmatters.com",
    "username": "username",
    "password": "password"
}

file = {
    "file_name": "file_name.csv",
    "encoding": "utf-8-sig"
}

logging = {
    "file_name": "log.log",
    "max_bytes": 16 * 1024 * 1024,  # 16mb is default
    "back_up_count": 2,
    "level": 10
    # Log Levels Integers
    # Critical: 50
    # Error:	40
    # Warning:	30
    # Info:     20
    # Debug:	10
    # Not Set:	0
}
