# upload
Тестовое задание Upload
### [Установка Django-приложения с помощью Ansible](#ansible)
### [Установка Django-приложения на сервер UBUNTU](#terminal)
### [Установка Django-приложения с помощью Docker](#docker)
### <a name="ansible">Установка Django-приложения с помощью Ansible</a>
Открываем терминал на клиенте.
Вводим следующие команды:

+  _cd ~/.ssh_

+  _ssh-keygen -t rsa_

+  _cat id_rsa.pub_ - выводим на экран публичный ключ, копируем в буфер Ctrl-C
  
Регистрируемся на сайте Vscale.io и создаем сервер. При создании сервера выбираем **Добавить ключ ssh**. В окне создания ключа вводим произвольное название и вставляем из буфера раннее скопированный ключ. Далее выбираем добавленный ключ и нажимаем **Создать сервер**.

Переходим в домашнюю папку:

+  _cd_ ~

На клиенте устанавливаем ansible

+  _sudo apt update_

+  _sudo apt install software-properties-common_

+  _sudo apt-add-repository --yes --update ppa:ansible/ansible_

+  _sudo apt install ansible_

Создаем файл hosts командой

 + _nano hosts_

> со следующими параметрами (IP или домен указываем для созданного сервера)

```
[servers]
test ansible_host=37.228.116.40 ansible_user=root
[servers:vars]
ansible_python_interpreter=/usr/bin/python3
```

Командой nano ansible.cfg - создаем файл ansible.cfg. В файле вводим:

```
[defaults]
inventory=hosts
```

Скачиваем файл site.yml по ссылке с помощью команды:

+ _wget 'https://raw.githubusercontent.com/grsln/upload/master/site.yml'_.

Перед запуском ansible в файле site.yml необходимо поменять параметры по умолчанию(пароль админки django, SECRET_KEY)

В терминале запускаем

+ _ansible-playbook site.yml_



### <a name="terminal">Установка Django-приложения на сервер UBUNTU</a>

Открываем терминал на клиенте.

Вводим следующие команды:

+ _cd ~/.ssh_

+ _ssh-keygen -t rsa_

> на все запросы нажимаем клавишу Enter

+ _cat id_rsa.pub_ - выводим на экран публичный ключ, копируем в буфер Ctrl-C

Регистрируемся на сайте Vscale.io и создаем сервер. При создании сервера выбираем **Добавить ключ ssh**. В окне создания ключа вводим произвольное название и вставляем из буфера раннее скопированный ключ. Далее выбираем добавленный ключ и нажимаем **Создать сервер**.

В окне терминала клиента вводим:

+ _ssh root@xxx.xxx.xxx.xxx_ (где xxx.xxx.xxx.xxx— IP созданного сервера).

Создаем пользователя

+ _adduser ruslan_

> вводим пароль для нового пользователя

Последовательно выполняем команды:

+ _usermod -aG sudo ruslan_

+ _su ruslan_

+ _sudo apt-get update_

+ _sudo apt install python3 python3-pip nginx python3-setuptools python3-venv git_

+ _mkdir ~/app_

+ _cd ~/app_

+ _git clone https://github.com/grsln/upload_

+ _cd upload_

+ _python3 -m venv venv_

+ _source venv/bin/activate_

+ _pip install wheel_

+ _pip install -r requirements.txt_

+ _pip install gunicorn_

Создаем и редактируем файл .env

+ _nano .env_

> содержимое файла .env

```
DEBUG=0
SECRET_KEY=<any_secret_key>
DJANGO_ALLOWED_HOSTS=<ip server>
```


+ _cd up_site_

+ _python manage.py makemigrations_

+ _python manage.py migrate_

Создаем суперпользователя вводим логин и пароль

+ _python manage.py createsuperuser_

+ _python manage.py collectstatic_

Создаем и редактируем файл

+ _sudo nano /etc/systemd/system/gunicorn.socket_

> содержимое файла gunicorn.socket

```
[Unit]
Description=gunicorn socket
[Socket]
ListenStream=/run/gunicorn.sock
[Install]
WantedBy=sockets.target
```

Создаем и редактируем файл

+ _sudo nano /etc/systemd/system/gunicorn.service_

> cодержимое файла gunicorn.service

```
[Unit]
Description=Gunicorn instance to serve upload
Requires=gunicorn.socket
After=network.target
[Service]
User=ruslan
Group=www-data
WorkingDirectory=/home/ruslan/app/upload/up_site
Environment="PATH=/home/ruslan/app/upload/venv/bin"
ExecStart=/home/ruslan/app/upload/venv/bin/gunicorn \
--workers 3 \
--bind unix:/run/gunicorn.sock \
up_site.wsgi:application
[Install]
WantedBy=multi-user.target
```

+ _sudo systemctl start gunicorn.socket_

+ _sudo systemctl enable gunicorn.socket_

+ _sudo rm /etc/nginx/sites-enabled/default_

Создаем и редактируем файл

+ _sudo nano /etc/nginx/sites-available/upload_

> содержимое файла upload(необходимо поменять IP)

```
server {
  listen 80;
  server_name 82.148.30.125;
  
  access_log /var/log/upload_access.log;
  error_log /var/log/upload_error.log;
  
  location = /favicon.ico { access_log off; log_not_found off; }
  
  location /static/ {
    root /home/ruslan/app/upload/up_site;
  }
  
  location /media/ {
    root /home/ruslan/app/upload/up_site;
  }
  
  location / {
    include proxy_params;
    proxy_pass http://unix:/run/gunicorn.sock;
  }
} 
```

+ _sudo ln -s /etc/nginx/sites-available/upload /etc/nginx/sites-enabled_

+ _sudo systemctl daemon-reload_

+ _sudo systemctl restart gunicorn_

+ _sudo systemctl restart nginx_

### <a name="docker">Установка Django-приложения с помощью Docker</a>

Открываем терминал на клиенте.

Вводим следующие команды:

+ _cd ~/.ssh_

+ _ssh-keygen -t rsa_

> на все запросы нажимаем клавишу Enter

+ _cat id_rsa.pub_ - выводим на экран публичный ключ, копируем в буфер Ctrl-C

Регистрируемся на сайте Vscale.io и создаем *Docker*-сервер. При создании сервера выбираем **Добавить ключ ssh**. В окне создания ключа вводим произвольное название и вставляем из буфера раннее скопированный ключ. Далее выбираем добавленный ключ и нажимаем **Создать сервер**.

В окне терминала клиента вводим:

+ _ssh root@xxx.xxx.xxx.xxx_ (где xxx.xxx.xxx.xxx— IP созданного сервера).

Скачиваем образы из Docker Hub.

+ _docker pull grsln/upload_web:latest_

+ _docker pull grsln/upload_nginx:latest_

Создаем docker-compose.yaml и вводим конфигурации

+ _nano docker-compose.yml_

```
version: '3.7'

services:
  web:
    image: grsln/upload_web:latest
    restart: always
    command: gunicorn up_site.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/home/up_site/web/static
      - media_volume:/home/up_site/web/media
    expose:
      - 8000
    env_file:
      - ./.env
  nginx:
    image: grsln/upload_nginx:latest
    restart: always
    volumes:
      - static_volume:/home/up_site/web/static
      - media_volume:/home/up_site/web/media
    ports:
      - 80:80
    depends_on:
      - web
volumes:
  static_volume:
  media_volume:
```

Создаем файл .env,  вводим IP-адрес docker-сервера и secret key 
+ _nano .env_

```
DEBUG=0
SECRET_KEY=<secret key >
DJANGO_ALLOWED_HOSTS=<ip>
```
Выполняем сборку и запуск контейнеров
+ _docker-compose  up -d --build_
