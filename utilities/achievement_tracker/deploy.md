# SECRET_KEY
```
python3 -c "import secrets; print(secrets.token_hex(32))"
```

# PASSWORD_HASH
```
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('мой_пароль'))"
```

# LOG DIR
```
mkdir -p /var/log/achievement_tracker
```


