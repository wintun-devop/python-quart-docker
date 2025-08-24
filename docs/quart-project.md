### quart official site
- https://pgjones.gitlab.io/quart/

### virtial environment set-up (window os)
```
python -m venv quart_env
```
### env installation
```
pip install python-dotenv
```
### 1st-phase-requirements
- quart jwt reference (https://quart-jwt-extended.readthedocs.io/en/latest/tokens_in_cookies/)
```
pip install quart quart-cors quart_jwt_extended
```

### quart bcrypt for password hasing
- reference (https://quart-bcrypt.readthedocs.io/en/latest/)
```
pip install quart-bcrypt
```
### quart run with default port number 5000
```
quart run --reload
```
### quart run with specific port number 8000
```
quart run --port 8000 --reload 
```

### create api step-by-step
- blue print on route
- regiseter blue-print on app

### Openssl Command for generate secret key
``
openssl rand -base64 32
``

# Running Cron(amazonlinux)
```
sudo yum install cronie -y
```
```
sudo systemctl start crond
```
```
sudo systemctl enable crond
```
### (@reboot /home/your_script_location > /home/your_log_location 2>&1 &)
```
@reboot /home/ec2-user/python-quart-dummy-api/quart-apis/server_run.sh > /home/ec2-user/python-quart-dummy-api/quart-apis/server_run.log 2>&1 &
```

