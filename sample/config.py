environment = {
    "url": "https://<instance>.xmatters.com",  # ensure that there's no / at the end
    "username": "username",
    "password": "password"
}

logging = {
    "file_name": "log.log",  # absolute path recommended for Windows, Linux can remain as is
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
