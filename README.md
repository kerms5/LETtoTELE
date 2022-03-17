# LETtoTELE

一个将LET新帖推送到teleBOT的项目。

虽然LET论坛提供RSS源，但是整个网站都添加了Cloudflare的金盾，所以直接使用RSS阅读器是获取不了的。这里使用了GitHub上的一个开源项目进行绕过。

基本逻辑：使用cloud越过cloudflare直接获取页面的信息，转交feedparser进行分析，在数据处理方面，由于LET论坛是按照最新回复时间进行排序，所以有可能两次获取重复的信息。为避免重复推送，添加了一个数据库验证过程，即只有此帖id不在数据库中才会进入推送流程，并且每个帖在推送完成之后都会自动写入数据库。

## 使用说明

首先你需要一个telegram bot，参考这篇文章注册。

然后，克隆本项目，修改`run.py`内的chat_id和bottoken为你设定的值。

```py
chat_id = ""  # Userid
token = ""  # 机器人 TOKEN
```

接着使用`pip install -r requirements.txt`安装依赖。

>如果出现安装lxml报错的情况，使用`sudo apt-get install libxml2-dev libxslt1-dev`安装lxml依赖。

使用`python3 run.py`即可运行服务。另外，可以使用screen命令在后台运行。

首次运行的初始化：基于上面的基本逻辑，如果你首次运行此服务，此服务将会把所有可以获取的历史记录全部发送到BOT，为了避免这种现象，默认将代码中的第43行进行了注释，运行一次之后，再取消注释，，重新运行，接下来发送的就全部是新帖了。