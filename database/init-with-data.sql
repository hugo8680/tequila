-- MySQL dump 10.13  Distrib 5.7.22, for Linux (x86_64)
--
-- Host: localhost    Database: tequila
-- ------------------------------------------------------
-- Server version	5.7.22-0ubuntu0.17.10.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `t_answer`
--

DROP TABLE IF EXISTS `t_answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_answer` (
  `aid` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `content` varchar(5120) NOT NULL,
  `has_read` tinyint(1) NOT NULL DEFAULT '0',
  `qid` int(6) unsigned NOT NULL,
  `uid` int(6) unsigned NOT NULL,
  PRIMARY KEY (`aid`),
  UNIQUE KEY `aid` (`aid`,`qid`),
  KEY `fk_answer_question_qid` (`qid`),
  KEY `fk_answer_user_uid` (`uid`),
  KEY `idx_answer` (`content`(8)),
  KEY `idx_answer_has_read` (`has_read`),
  CONSTRAINT `fk_answer_question_qid` FOREIGN KEY (`qid`) REFERENCES `t_question` (`qid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_answer_user_uid` FOREIGN KEY (`uid`) REFERENCES `t_user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=100012 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_answer`
--

LOCK TABLES `t_answer` WRITE;
/*!40000 ALTER TABLE `t_answer` DISABLE KEYS */;
INSERT INTO `t_answer` VALUES (100000,1,'2018-05-24 03:31:54','2018-05-24 03:53:07','<p>嘎嘎，原来貌似只要给类加上stream_request_body装饰器，data_received就是异步的了，只管在data_received里面进行写文件就好了<br></p><p>==================old================</p><p>实在没办法，nginx的upload_module在高版本编不过去，网上又找不到可用的py库，我就这样了</p><p>ʕ⊙ᴥ⊙ʔ  </p><p>至少是没堵着。。。</p><pre><code><span class=\"kn\">from</span> <span class=\"nn\">tornado.web</span> <span class=\"k\">import</span> <span class=\"n\">RequestHandler</span>\n<span class=\"kn\">from</span> <span class=\"nn\">tornado</span> <span class=\"k\">import</span> <span class=\"n\">gen</span>\n<span class=\"kn\">from</span> <span class=\"nn\">tornado.web</span> <span class=\"k\">import</span> <span class=\"n\">stream_request_body</span>\n<span class=\"kn\">import</span> <span class=\"nn\">time</span>\n<span class=\"kn\">import</span> <span class=\"nn\">random</span>\n\n\n<span class=\"nd\">@stream_request_body</span>\n<span class=\"k\">class</span> <span class=\"nc\">A</span><span class=\"p\">(</span><span class=\"n\">RequestHandler</span><span class=\"p\">):</span>\n    <span class=\"k\">def</span> <span class=\"nf\">initialize</span><span class=\"p\">(</span><span class=\"bp\">self</span><span class=\"p\">):</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">fp</span> <span class=\"o\">=</span> <span class=\"nb\">open</span><span class=\"p\">(</span><span class=\"s1\">\'xxxx.tmp\'</span><span class=\"p\">,</span><span class=\"s1\">\'wb\'</span><span class=\"p\">)</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">size</span> <span class=\"o\">=</span> <span class=\"mi\">0</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">id</span> <span class=\"o\">=</span> <span class=\"n\">random</span><span class=\"o\">.</span><span class=\"n\">randint</span><span class=\"p\">(</span><span class=\"mi\">0</span><span class=\"p\">,</span><span class=\"mi\">100</span><span class=\"p\">)</span>\n\n    <span class=\"k\">async</span> <span class=\"k\">def</span> <span class=\"nf\">post</span><span class=\"p\">(</span><span class=\"bp\">self</span><span class=\"p\">):</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">set_header</span><span class=\"p\">(</span><span class=\"s1\">\'Content-Type\'</span><span class=\"p\">,</span> <span class=\"s1\">\'application/json;charset=utf-8\'</span><span class=\"p\">)</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">finish</span><span class=\"p\">(</span><span class=\"s1\">\'{\"msg\":\"ok\"}\'</span><span class=\"p\">)</span>\n        <span class=\"k\">await</span> <span class=\"n\">gen</span><span class=\"o\">.</span><span class=\"n\">sleep</span><span class=\"p\">(</span><span class=\"mi\">0</span><span class=\"p\">)</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">fp</span><span class=\"o\">.</span><span class=\"n\">close</span><span class=\"p\">()</span>\n\n    <span class=\"k\">async</span> <span class=\"k\">def</span> <span class=\"nf\">data_received</span><span class=\"p\">(</span><span class=\"bp\">self</span><span class=\"p\">,</span> <span class=\"n\">chunk</span><span class=\"p\">):</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">size</span> <span class=\"o\">+=</span> <span class=\"nb\">len</span><span class=\"p\">(</span><span class=\"n\">chunk</span><span class=\"p\">)</span>\n        <span class=\"nb\">print</span><span class=\"p\">(</span><span class=\"n\">time</span><span class=\"o\">.</span><span class=\"n\">time</span><span class=\"p\">(),</span> <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">id</span><span class=\"p\">,</span> <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">size</span><span class=\"p\">)</span>\n        <span class=\"bp\">self</span><span class=\"o\">.</span><span class=\"n\">fp</span><span class=\"o\">.</span><span class=\"n\">write</span><span class=\"p\">(</span><span class=\"n\">chunk</span><span class=\"p\">)</span>\n        <span class=\"k\">await</span> <span class=\"n\">gen</span><span class=\"o\">.</span><span class=\"n\">sleep</span><span class=\"p\">(</span><span class=\"mi\">0</span><span class=\"p\">)</span></code></pre><h1><br></h1>',1,100000,100001),(100001,1,'2018-05-24 03:34:56','2018-05-24 03:53:10','<p>这个系统用tornado搭建本身就选择错误。原因如下：</p><p>1. 对于读取上传文件，tornado的官网上有说过，对于文件上传，tornado是直接全部读到内存中，再进行处理，也就是说，文件越大，文件越多，你的资源占用就越多。官网推荐用 nginx 的upload  module 来处理</p><p>2. 写文件这个操作，如果你用的是机械磁盘，本身就是同步的。因为只有一个磁头，每次的寻址都是同步的。所以，tornado的写文件操作无法异步。</p><p>如果一定用tornado，需要这么做：</p><p>1. 整个系统用nginx+tornado [+另外的server]</p><p>2. 对于文件上传，采用nginx upload module，nginx负责文件的上传，tornado只负责进行文件的cp和mv</p><p>3. 如果你的文件上传后有后续复杂的io操作。比方说：读取文件里面的内容，找出之前的某个相关文件，并且合并，再重新写入。那么需要一个另外的server，专门负责这个。</p><p>4. 对于第3点，如果你采用非机械磁盘，应该就没有必要了。</p>',1,100000,100002),(100002,0,'2018-05-24 03:35:52','2018-05-24 03:35:52','<p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">如果仅仅是上传文件，相关的逻辑很少，使用nginx+module处理就很好</span></p><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">如果上传文件还有较多的逻辑处理，nodejs的非阻塞io也非常好用。</span></p><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">如果一定要用torado，那么加锁的开销其实不大，每秒进行lock十万次应该是没问题的</span></p>',1,100000,100003),(100003,0,'2018-05-24 03:36:30','2018-05-24 03:36:30','<p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">Tornado 真是io伤不起啊, 一旦阻塞整个服务都block..</span></p><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">所以耗时的任务采用异步httpclient交给后端server处理..或采用专业的MQ解决你说的锁问题</span></p>',1,100000,100004),(100004,0,'2018-05-24 03:39:20','2018-05-24 03:39:20','<p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">self.request.remote_ip 这样就可以了，楼主试试。<img alt=\"tornado.png\" src=\"http://127.0.0.1:8000/pics/20180524/100cb5a1-46e1-43ce-822d-5de26460e55atornado.png\" width=\"286\" height=\"72\"></span><br></p>',1,100001,100001),(100005,0,'2018-05-24 03:40:09','2018-05-24 03:40:09','<p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">当你是直接访问一个tornado instance的时候，通过self.request.remote_ip就可以访问到client IP;&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">当你是通过反向代理来访问的时候，你的HTTPServer构造参数需要加一个xheaders=True&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">http_server = HTTPServer(Application(), xheaders=True) , 这样你就可以通过self.request.remote_ip来获得期望的IP&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">可以参考下tornado源码，希望对你有帮助 :)&nbsp;</span></p>',1,100001,100002),(100006,0,'2018-05-24 03:40:53','2018-05-24 03:40:53','<p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">补充：如果应用像 Hello World 中的示例一样没用到 HTTPServer，&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\"></span></p><p><code><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">if __name__ == \"__main__\":&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">application.listen(8888)&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">tornado.ioloop.IOLoop.instance().start()&nbsp;</span></p></code></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\"></span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">那么可以把 xheaders=True 传入 application.listen 里，该 method 的代码是：&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\"></span></p><p><code><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">def listen(self, port, address=\"\", **kwargs):&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">from tornado.httpserver import HTTPServer&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">server = HTTPServer(self, **kwargs)&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">server.listen(port, address)</span></p></code></p>',1,100001,100000),(100007,1,'2018-05-24 03:42:59','2018-05-24 03:52:39','<p>楼主的问题描述的不是很清楚啊，请问你遇到了什么问题？</p>',1,100002,100003),(100008,0,'2018-05-24 03:47:29','2018-05-24 03:47:29','<p>C#中的事件其实就是一个特殊的多播委托。比如写一段代码：<br></p><pre><code><span class=\"k\">class</span> <span class=\"nc\">Program</span>\n<span class=\"p\">{</span>\n	<span class=\"k\">public</span> <span class=\"k\">delegate</span> <span class=\"k\">void</span> <span class=\"nf\">SendHandler</span><span class=\"p\">(</span><span class=\"kt\">string</span> <span class=\"n\">str</span><span class=\"p\">);</span>\n	<span class=\"k\">public</span> <span class=\"k\">event</span> <span class=\"n\">SendHandler</span> <span class=\"n\">SendEvent</span><span class=\"p\">;</span>\n	<span class=\"k\">static</span> <span class=\"k\">void</span> <span class=\"nf\">Main</span><span class=\"p\">(</span><span class=\"kt\">string</span><span class=\"p\">[]</span> <span class=\"n\">args</span><span class=\"p\">)</span>\n	<span class=\"p\">{</span> <span class=\"p\">}</span>\n<span class=\"p\">}</span>\n</code></pre><p>编译后我们用ILDASM.EXE打开那个exe看看就会发现其实SendHandler委托被编译为了一个叫做SendHandler的类，</p><p><br></p><p><img alt=\"啊啊啊.jpg\" src=\"http://127.0.0.1:8000/pics/20180524/45da56c1-5077-47cc-8beb-328d5b61ecbf啊啊啊.jpg\" width=\"338\" height=\"215\"><br></p><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\"></span></p><p>SendEvent事件则是被编译成了包含一个add_前缀和一个remove_前缀的的<b>代码段</b>（倒三角）。<br></p><pre><code><span class=\"o\">.</span><span class=\"k\">event</span> <span class=\"n\">Program</span><span class=\"o\">/</span><span class=\"n\">SendHandler</span> <span class=\"n\">SendEvent</span>\n<span class=\"o\">{</span>\n  <span class=\"o\">.</span><span class=\"n\">addon</span> <span class=\"n\">instance</span> <span class=\"k\">void</span> <span class=\"n\">Program</span><span class=\"o\">::</span><span class=\"n\">add_SendEvent</span><span class=\"o\">(</span><span class=\"k\">class</span> <span class=\"n\">Program</span><span class=\"o\">/</span><span class=\"n\">SendHandler</span><span class=\"o\">)</span>\n  <span class=\"o\">.</span><span class=\"n\">removeon</span> <span class=\"n\">instance</span> <span class=\"k\">void</span> <span class=\"n\">Program</span><span class=\"o\">::</span><span class=\"n\">remove_SendEvent</span><span class=\"o\">(</span><span class=\"k\">class</span> <span class=\"n\">Program</span><span class=\"o\">/</span><span class=\"n\">SendHandler</span><span class=\"o\">)</span>\n<span class=\"o\">}</span> <span class=\"c1\">// end of event Program::SendEvent</span>\n</code></pre><p>add_前缀的方法其实是通过调用Delegate.Combine()方法来实现的，组成了一个多播委托。remove_就是调用Delegate.Remove()方法，用于移除多播委托中的某个委托。</p><p>好了，前面的都不是废话，你还会看到有一个SendEvent的<b>字段</b>（蔚蓝色菱形）</p><pre><code><span class=\"p\">.</span><span class=\"n\">field</span> <span class=\"k\">private</span> <span class=\"k\">class</span> <span class=\"nc\">Program</span><span class=\"p\">/</span><span class=\"n\">SendHandler</span> <span class=\"n\">SendEvent</span>\n</code></pre><p>说事件是一个特殊的多播委托，那么事件比较特殊的地方在于这里，事件具有一个私有的委托类型的字段，其存储了对事件处理方法的引用。而add_前缀方法和remove_前缀方法起到的就是类似C#属性访问器中get_和set_方法的作用，使用事件访问私有委托。</p><p><b>简而言之，事件就是用来访问私有的委托字段，让应用程序的代码更加的安全。</b></p>',1,100003,100003),(100009,1,'2018-05-24 03:50:14','2018-05-24 03:52:27','<p>首先，你可以关注下C# 4里引入的协变逆变，这样可能引入一个IBase&lt;T&gt;就可以干活。</p><p>其次，Handle&lt;T&gt;(Base&lt;T&gt;[] itemList) 也是一个常见的签名。</p>',1,100004,100002),(100010,1,'2018-05-24 03:50:49','2018-05-24 03:52:30','<p>Base&lt;string&gt;和Base&lt;int&gt;可以认为是两个毫不相干的类型。</p><p>如果一定要产生联系，需要加入一个公共基类像这样：</p><pre><code>Base&lt;T&gt; : Base\n</code></pre><p>那么这时候，Base&lt;string&gt;和Base&lt;int&gt;就有了共同的基类Base了。</p><p>当然，C# 4加入了泛型接口的协变和逆变，不过这和你的泛型类型没啥关系。</p>',1,100004,100004),(100011,0,'2018-05-24 03:52:02','2018-05-24 03:52:02','<p>StringChild 赋值给 Base&lt;String&gt;是完全没问题的，因为是继承关系。</p><p>但是 Base&lt;String&gt; 并不能赋值给 Base&lt;Object&gt;，尽管 String 是 Object 子类。这个刚开始的时候可能有点想不通，举个简单的例子：楼主(String)比我(Object)小，并不能推出楼主的父亲(Base&lt;String&gt;)就比我父亲(Base&lt;Object&gt;)小。</p><p>楼主可以看一下Eric Lippert 关于Covariance and Contravariance的这个系列 <a href=\"https://link.zhihu.com/?target=http%3A//blogs.msdn.com/b/ericlippert/archive/tags/covariance%2Band%2Bcontravariance/\" target=\"_blank\">http://blogs.msdn.com/b/ericlippert/archive/tags/covariance+and+contravariance/</a>，相信会有帮助的。</p>',1,100004,100003);
/*!40000 ALTER TABLE `t_answer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_group`
--

DROP TABLE IF EXISTS `t_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_group` (
  `group_type` int(1) NOT NULL DEFAULT '0',
  `group_name` varchar(12) NOT NULL,
  `description` varchar(40) DEFAULT NULL,
  UNIQUE KEY `group_type` (`group_type`,`group_name`),
  KEY `idx_group` (`group_name`(4))
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_group`
--

LOCK TABLES `t_group` WRITE;
/*!40000 ALTER TABLE `t_group` DISABLE KEYS */;
INSERT INTO `t_group` VALUES (0,'user','normal user'),(1,'admin','admin user'),(2,'superuser','super admin user');
/*!40000 ALTER TABLE `t_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_question`
--

DROP TABLE IF EXISTS `t_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_question` (
  `qid` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL DEFAULT '0',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `abstract` varchar(24) NOT NULL,
  `content` varchar(10240) NOT NULL,
  `view_count` int(11) NOT NULL DEFAULT '0',
  `answer_count` int(11) NOT NULL DEFAULT '0',
  `adopted_count` int(1) NOT NULL DEFAULT '0',
  `uid` int(6) unsigned NOT NULL,
  `tid` int(6) unsigned NOT NULL,
  PRIMARY KEY (`qid`),
  UNIQUE KEY `qid` (`qid`,`uid`,`tid`),
  KEY `fk_question_user_uid` (`uid`),
  KEY `fk_question_tag_tid` (`tid`),
  KEY `idx_question` (`abstract`(8),`content`(8)),
  CONSTRAINT `fk_question_tag_tid` FOREIGN KEY (`tid`) REFERENCES `t_tag` (`tid`),
  CONSTRAINT `fk_question_user_uid` FOREIGN KEY (`uid`) REFERENCES `t_user` (`uid`)
) ENGINE=InnoDB AUTO_INCREMENT=100005 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_question`
--

LOCK TABLES `t_question` WRITE;
/*!40000 ALTER TABLE `t_question` DISABLE KEYS */;
INSERT INTO `t_question` VALUES (100000,0,'2018-05-24 03:27:24','2018-05-24 03:53:10','Tornado 异步读写文件的方法？','<p><b>大家好，</b><br></p><p>我现在正在使用Tornado开发一个文件上传应用。当通过Tornado主线程异步获取到用户上传的文件数据后，我需要把数据写入到文件系统中。</p><p>1. 如果为每个文件的写操作单独开一个线程/进程，由于可能同时写很多文件，大量的线程/进程对服务器会是很大的开销，而且Tornado也不建议乱开线程/进程；</p><p>2. 如果把所有待写入的数据放到队列中，然后用一个线程周期性地从队列中获取数据并写入到文件系统中，则会涉及到对队列的加锁问题。而锁的引入势必又会拖慢Tornado的速度（因为Tornado必须获取锁后才能把数据写到队列中）。</p><p>3. 一个更理想的做法是采用类似Tornado读写socket的epoll模型，这样既可以不开线程/进程，又不会阻塞，但普通文件的读写又不支持epoll（即不能设置为non-block）。</p><p>所以想请问大家，像这种异步读写文件的问题一般是怎么解决的呢？<span style=\"color: rgb(227, 55, 55);\">谢谢</span>！</p>',3,4,2,100000,100000),(100001,0,'2018-05-24 03:38:17','2018-05-24 03:40:53','Tornado2.3获取IP错误！什么原因？','<p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">最近将框架升级到2.3，发现获取请求的IP地址出现错误！&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">我在Request中读取self.remote_ip，不管是正常访问还是代理方式的访问，其结果都是127.0.0.1，而我直接获取self.request.headers[\'X-Real-Ip\']，结果却正是我想要的。&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">不知道是不是自己设置options时出错，还是自己nginx代理出错？&nbsp;</span></p><p><span style=\"color: rgb(17, 17, 17); font-size: 14px;\">莫非是bug？</span></p><p><img alt=\"tornado.png\" src=\"http://127.0.0.1:8000/pics/20180524/2d78f262-bbbb-4995-b07a-40180638a35dtornado.png\" width=\"286\" height=\"72\"><br></p>',2,3,0,100004,100000),(100002,0,'2018-05-24 03:42:13','2018-05-24 03:52:39','tornado HTML页面处理 问题','<p><span style=\"font-size: 14px;\">tornado HTML中报这样的错：</span></p><p><span style=\"font-size: 14px;\">File \"online/post_html.generated.py\", line 13, in _tt_execute</span></p><p><span style=\"font-size: 14px;\">_tt_tmp = gen_meid or \'手机串号为空\' # online/post.html:27 (via _base.html:15)</span></p><p><span style=\"font-size: 14px;\">NameError: global name \'gen_meid\' is not defined</span></p><p><span style=\"font-size: 14px;\">我如何在html中判断gen_meid这个参数传过来没有</span></p>',1,1,1,100001,100000),(100003,0,'2018-05-24 03:44:50','2018-05-24 03:47:29','c#中委托和事件？','<p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">总是感觉委托和事件没什么区别，调用事件不就是相当于调用多个委托么？</span><br></p>',1,1,0,100003,100001),(100004,0,'2018-05-24 03:49:42','2018-05-24 03:52:30','C# 泛型转换问题？','<p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">有这么个类：</span></p><pre><code><span class=\"k\" style=\"font-weight: 600;\">class</span> <span class=\"nc\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">Base</span><span class=\"p\">&lt;</span><span class=\"n\">T</span><span class=\"p\">&gt;{}</span>\n</code></pre><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">有若干个子类：</span></p><pre><code><span class=\"k\" style=\"font-weight: 600;\">class</span> <span class=\"nc\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">StringChild</span> <span class=\"p\">:</span> <span class=\"n\">Base</span><span class=\"p\">&lt;</span><span class=\"n\">String</span><span class=\"p\">&gt;{}</span>\n<span class=\"k\" style=\"font-weight: 600;\">class</span> <span class=\"nc\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">IntChild</span> <span class=\"p\">:</span> <span class=\"n\">Base</span><span class=\"p\">&lt;</span><span class=\"kt\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">int</span><span class=\"p\">&gt;{}</span>\n<span class=\"p\">...</span>\n</code></pre><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">然后有个处理类：</span></p><pre><code><span class=\"k\" style=\"font-weight: 600;\">class</span> <span class=\"nc\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">Handler</span><span class=\"p\">{}</span>\n</code></pre><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">这个处理类有个功能是处理一个由很多StringChild、IntChild等组成的数组：</span></p><pre><code><span class=\"k\" style=\"font-weight: 600;\">public</span> <span class=\"k\" style=\"font-weight: 600;\">void</span> <span class=\"nf\" style=\"font-weight: 600; color: rgb(241, 64, 60);\">handle</span><span class=\"p\">(</span><span class=\"n\">Base</span><span class=\"p\">&lt;</span><span class=\"kt\" style=\"font-weight: 600; color: rgb(23, 81, 153);\">object</span><span class=\"p\">&gt;[]</span> <span class=\"n\">itemList</span><span class=\"p\">)</span>\n</code></pre><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">但是转换却报错：</span></p><pre><code>Base&lt;object&gt; base = (Base&lt;object&gt;)item[i];\n</code></pre><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">为啥 StringChild 等的实例却无法转换为 Base&lt;object&gt;？那我应该怎么写才能符合我的要求？</span></p><p><span style=\"color: rgb(26, 26, 26); font-size: 15px;\">C#初学，打扰各位大神了。有空的麻烦帮我解答一下。</span></p>',3,3,2,100001,100001);
/*!40000 ALTER TABLE `t_question` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_tag`
--

DROP TABLE IF EXISTS `t_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_tag` (
  `tid` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `tag_name` varchar(12) NOT NULL,
  PRIMARY KEY (`tid`),
  UNIQUE KEY `tid` (`tid`),
  KEY `idx_tag` (`tag_name`(2))
) ENGINE=InnoDB AUTO_INCREMENT=100003 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_tag`
--

LOCK TABLES `t_tag` WRITE;
/*!40000 ALTER TABLE `t_tag` DISABLE KEYS */;
INSERT INTO `t_tag` VALUES (100000,'2018-05-24 03:25:44','2018-05-24 03:25:44',1,'Python'),(100001,'2018-05-24 03:25:44','2018-05-24 03:25:44',1,'C#'),(100002,'2018-05-24 03:25:44','2018-05-24 03:25:44',1,'Docker');
/*!40000 ALTER TABLE `t_tag` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `t_user`
--

DROP TABLE IF EXISTS `t_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `t_user` (
  `uid` int(6) unsigned NOT NULL AUTO_INCREMENT,
  `status` tinyint(1) NOT NULL DEFAULT '1',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `username` varchar(12) NOT NULL,
  `email` varchar(40) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `password` varchar(40) NOT NULL,
  `point` int(4) DEFAULT '0',
  `sex` tinyint(1) DEFAULT '1',
  `address` varchar(60) DEFAULT NULL,
  `group_type` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`uid`),
  UNIQUE KEY `uid` (`uid`,`username`,`email`,`phone`),
  KEY `fk_user_group_group_type` (`group_type`),
  KEY `idx_user` (`username`(8),`email`(8),`phone`(8)),
  CONSTRAINT `fk_user_group_group_type` FOREIGN KEY (`group_type`) REFERENCES `t_group` (`group_type`)
) ENGINE=InnoDB AUTO_INCREMENT=100005 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `t_user`
--

LOCK TABLES `t_user` WRITE;
/*!40000 ALTER TABLE `t_user` DISABLE KEYS */;
INSERT INTO `t_user` VALUES (100000,1,'2018-05-24 03:25:44','2018-05-24 03:25:44','hugo','zhang8680@outlook.com',NULL,'18f3e922a1d1a9a140efbbe894bc829eeec260d8',0,1,NULL,2),(100001,1,'2018-05-24 03:27:53','2018-05-24 03:53:07','john',NULL,NULL,'18f3e922a1d1a9a140efbbe894bc829eeec260d8',1,1,NULL,0),(100002,1,'2018-05-24 03:33:49','2018-05-24 03:53:10','leslie',NULL,NULL,'18f3e922a1d1a9a140efbbe894bc829eeec260d8',2,1,NULL,0),(100003,1,'2018-05-24 03:35:31','2018-05-24 03:52:39','tornado',NULL,NULL,'18f3e922a1d1a9a140efbbe894bc829eeec260d8',1,1,NULL,0),(100004,1,'2018-05-24 03:36:24','2018-05-24 03:52:30','iloveyou',NULL,NULL,'18f3e922a1d1a9a140efbbe894bc829eeec260d8',1,1,NULL,0);
/*!40000 ALTER TABLE `t_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-05-24 11:54:21
