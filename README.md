## 安装
使用pip安装： <br/>
`pip install -r requirements.txt`

## django基本配置

### 运行

然后修改`cloundcmdb/settings/settings.py，修改数据库配置，更改为自己本地的数据库名、IP、账号密码和端口，如下所示：
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'root'
    }
}
```
修改REDIS配置，将IP更改为自己本地的REDIS IP，如下所示：
```python
CACHES = {
    "default": {  # 默认
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
    "session": {  # session
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    },
}
```

修改CELERY配置，将IP更改为自己本地的REDIS IP，如下所示：

```python
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/2'  # Broker配置，使用Redis作为消息中间件
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'  # BACKEND配置，这里使用redis
```

创建celery定时任务添加

```
CELERY_BEAT_SCHEDULE = {
    'my_task': {
        'task': 'apps.libary.tasks.return_reminder',
        'schedule': crontab(minute=0, hour=8),  # 每天8:00执行
    },
}
```

邮件发送<br/>
修改apps\libary\tasks.py文件`smtp_host`,`sender_email`,`mail_pass`设置对应的邮箱SMTP服务地址，发送人邮箱地址，发送人邮箱SMTP授权码

### 创建数据库

```mysql
CREATE DATABASE `library` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

然后终端下执行:

```shell
python manage.py makemigrations
python manage.py migrate
```

**注意：**
在使用 python manage.py 之前需要确定你系统中的 python 命令是指向 python 3.6 及以上版本的。如果不是如此，请使用以下两种方式中的一种：
* 修改 `manage.py `第一行 `#!/usr/bin/env python `为 `#!/usr/bin/env python3`
* 直接使用`python3 manage.py`

### 创建超级用户
终端下执行：<br/>
`python manage.py createsuperuser`

### 开始运行

`python manage.py runserver`

### 启动celery worker

在Windows的终端上启动：<br/>
`celery -A settings worker -l info -P eventlet` <br/>
celery版本4x用以下命令<br/>
`celery -A settings worker -l info -P solo` <br/>
在Linux的终端上启动：<br/>
`celery -A settings worker -l info`

### 启动celery beat
启动命令：<br/>
`celery -A settings beat -l info`
