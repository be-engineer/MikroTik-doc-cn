# 定制要求

- hotspot强制门户

## 介绍

你可以为每个 HotSpot 服务器创建一组完全不同的小服务程序页面，在 HotSpot 服务器配置文件 /ip hotspot配置文件的“html-override-directory”属性中指定目录。 创建服务器配置文件后，默认的小服务程序页面会立即复制到目录“hotspot”目录中。 可以使用 FTP 客户端连接到路由器来访问该目录。 可以使用手册这一部分中的信息复制此目录并根据需要修改页面。 建议手动编辑文件，因为自动 HTML 编辑工具可能会通过删除变量或其他重要部分来破坏页面。 完成内容修改后，你需要将此修改后的内容上传到hotspot路由器上的某个自定义目录，并将前面提到的属性“html-override-directory”值作为此新自定义 HTML 目录的路径。

**注意：** 如果“html-override-directory”值路径丢失或为空，则热点服务器将恢复为默认 HTML 文件。

## 可用页面

向用户显示的主要 HTML 小服务程序页面：

- **redirect.html** - 将用户重定向到另一个 url（例如，登录页面）
- **login.html** - 向用户显示的登录页面要求用户名和密码。 该页面可能采用以下参数：
  - **username** - 用户名
  - **password** - 纯文本密码（ PAP 身份验证）或 chap-id 变量、密码和 CHAP 质询的 MD5 哈希（ CHAP 身份验证）。 该值用作试用用户的电子邮件地址
  - **dst** - 重定向前请求的原始 URL。 这将在成功登录时打开
  - **popup** - 是否在成功登录时弹出状态窗口
  - **radius<id>** - 以文本字符串形式把用 <id> 标识的属性发送到 RADIUS 服务器（如果使用 RADIUS 身份验证；否则会丢失）
  - **radius<id>u** - 以无符号整数形式把用 <id> 标识的属性发送到 RADIUS 服务器（如果使用 RADIUS 身份验证；否则会丢失）
  - **radius <id>-<vnd-id>** - 把用 <id> 和供应商 ID <vnd-id> 标识的属性以文本字符串形式发送到 RADIUS 服务器(如果使用 RADIUS 身份验证；否则会丢失)
  - **radius<id\>-<vnd-id>u** - 以无符号整数形式向 RADIUS 服务器发送由 <id> 和供应商 ID <vnd-id> 标识的属性（如果使用 RADIUS 身份验证；否则会丢失）
- **md5.js** - MD5 密码散列的 JavaScript。 与http-chap登录方式配合使用
- **alogin.html** - 客户端登录后显示的页面。它弹出状态页面并将浏览器重定向到最初请求的页面（在被重定向到 HotSpot 登录页面之前）
- **status.html** - 状态页面，显示客户端的统计信息。 可以自动显示通告
- **logout.html** - 注销页面，在用户注销后显示。 显示有关已完成会话的最终统计信息。 此页面可能采用以下附加参数：
  - **erase-cookie** - 是否在注销时从 HotSpot 服务器中删除 cookie（使得下次无法从同一浏览器使用 cookie 登录，可能在多用户环境中有用）
- **error.html** - 错误页面，仅在出现致命错误时显示

如果需要更多控制，还可以使用其他一些页面：

- **rlogin.html** - 页面，如果需要客户端授权才能访问该 URL，则将客户端从其他 URL 重定向到登录页面
- **rstatus.html** - 类似于 rlogin.html，仅在客户端已经登录且原始 URL 未知的情况下使用
- **radvert.html** - 将客户端重定向到预定的通告链接
- **flogin.html** - 如果发生错误则显示，而不是 login.html（例如无效的用户名或密码）
- **fstatus.html** - 如果请求状态页面，但客户端未登录则显示而不是重定向
- **flogout.html** - 如果请求注销页面但客户端未登录则显示而不是重定向

### Serving 小服务程序页面

HotSpot 小服务程序识别 5 种不同的请求类型：

1. **request for a remote host**

   - 如果用户已登录并且要显示通告，则显示 radvert.html。 此页面重定向到预定的通告页面
   - 如果用户已登录且没有为该用户安排通告，则提供请求的页面
   - 如果用户未登录，但围墙花园允许目标主机，则请求也会被处理
   - 如果用户未登录，且围墙花园不允许目标主机，则显示 rlogin.html； 如果没有找到 rlogin.html，则使用 redirect.html 重定向到登录页面

2. **在HotSpot主机上请求“/”**

   - 如果用户已登录，则显示 rstatus.html； 如果没有找到 rstatus.html，则使用 redirect.html 重定向到状态页面
   - 如果用户未登录，则显示 rlogin.html； 如果没有找到 rlogin.html，则使用 redirect.html 重定向到登录页面
  
3. **请求“/login”页面**

   - 如果用户已成功登录（或已经登录），则显示 alogin.html； 如果未找到 alogin.html，则使用 redirect.html 重定向到最初请求的页面或状态页面（以防未给出原始目标页面）
   - 如果用户未登录（未提供用户名，未出现错误消息），则显示 login.html
   - 如果登录程序失败（提供错误消息），则显示 flogin.html； 如果找不到 flogin.html，则使用 login.html
   - 如果出现致命错误，则显示 error.html

4. **请求“/status”页面**

   - 如果用户已登录，则显示 status.html
   - 如果用户未登录，则显示 fstatus.html； 如果找不到 fstatus.html，则使用 redirect.html 重定向到登录页面

5. **请求“/logout”页面**

   - 如果用户已登录，则显示 logout.html
   - 如果用户未登录，则显示 flogout.html； 如果找不到 flogout.html，则使用 redirect.html 重定向到登录页面

**注意：** 如果使用存储在路由器 FTP 服务器上的页面无法满足请求，则会显示错误 404

自定义 HotSpot 身份验证页面的外观有多种可能性：

- 页面容易修改。 它们存储在路由器的 FTP 服务器上，位于你为各自的 HotSpot 服务器配置文件选择的目录中。
- 通过更改客户端发送到 HotSpot 小服务程序的变量，可以将关键字计数减少到一个（用户名或密码；例如，客户端的 MAC 地址可以用作其他值）甚至为零（许可协议 ; 一些对所有用户通用的预定义值或客户端的 MAC 地址可以用作用户名和密码）
- 注册可能发生在不同的服务器上（例如，在能够对信用卡收费的服务器上）。 客户端的 MAC 地址可以传递给它，因此不需要手动写入此信息。 注册后，服务器应更改 RADIUS 数据库，使客户端能够登录一段时间。

要在 HTML 文件的某个地方插入变量，使用 $(var_name) 语法，其中“var_name”是变量的名称（不带引号）。 此结构可用于任何以“/”、“/login”、“/status”或“/logout”访问的 HotSpot HTML 文件，以及存储在 HotSpot 服务器上的任何文本或 HTML（.txt、.htm 或 .html）文件 （流量计数器除外，它们仅在状态页面中可用，以及 **error**、**error-orig**、**chap-id**、**chap-challenge** 和 **popup** 变量，仅在登录页面中可用）。 例如，要显示登录页面的链接，可以使用以下结构：

```
<a href="$(link-login)">login</a>

```

### 变量

所有小服务程序 HTML 页面都使用变量来显示用户特定的值。 变量名只出现在 小服务程序页面的 HTML 源代码中——它们会被 HotSpot 小服务程序自动替换为各自的值。 对于大多数变量，括号中都有一个可能值的示例。 所有描述的变量在所有小服务程序页面中都有效，但其中一些变量在访问时可能为空（例如，在用户登录之前没有正常运行时间）。

#### 可用变量列表

**注意：** 一些变量使用硬编码的http URL，如果用https，可以用其他方式构造链接，例如$link-status，可以使用https://$(hostname)/$(target-dir)状态

**常用服务器变量：**

- **hostname** - HotSpot小服务程序 ("[hotspot.example.net](http://hotspot.example.net/)") 的 DNS 名称或 IP 地址（如果未提供 DNS 名称）
- **identity** - RouterOS 身份名称（“MikroTik”）
- **login-by** - 用户使用的身份验证方法
- **plain-passwd** - 是否允许 HTTP-PAP 登录方法的“是/否”表示（“否”）
- **server-address** - 热点服务器地址（“10.5.50.1:80”）
- **ssl-login** - 是否使用 HTTPS 方法访问该小服务程序页面的“是/否”表示（“否”）
- **server-name** - HotSpot 服务器名称（在 /ip hotspot菜单中设置，作为名称属性）

**链接:**

- **link-login** -链接到登录页，包括请求的原始 URL("[http://10.5.50.1/login?dst=http://www.example.com/](http://10.5.50.1/login?dst=http://www.example.com/)")
- **link-login-only** - 链接到登录页，不包括请求的原始 URL ("[http://10.5.50.1/login](http://10.5.50.1/login)")
- **link-logout** - 链接到退出页 ("[http://10.5.50.1/logout](http://10.5.50.1/logout)")
- **link-status** - 链接到状态页 ("[http://10.5.50.1/status](http://10.5.50.1/status)")
- **link-orig** - 已请求的原始URL("[http://www.example.com/](http://www.example.com/)")

**一般客户信息：**

- **domain** - 用户的域名（“[example.com](http://example.com/)”）
- **interface-name** - 物理 HotSpot 接口名称（如果是桥接接口，将返回实际的桥接端口名称）
- **ip** - 客户端的 IP 地址（“10.5.50.2”）
- **logged-in** - 如果用户已登录则为“是”，否则 - “否”（“是”）
- **mac** - 用户的 MAC 地址（“01:23:45:67:89:AB”）
- **trial** - 用户是否有权访问试用时间的“是/否”表示。 如果用户试用时间已过，值为“否”
- **username** - 用户名（“John”）
- **host-ip** - 来自 /ip hotspot主机表的客户端 IP 地址
- **vlan-id** - 表示连接客户端的 VLAN 接口的 ID

**用户状态信息：**

- **idle-timeout** - 空闲超时（“20m”或“”）
- **idle-timeout-secs** - 以秒为单位的空闲超时（如果有这样的超时，则为“88”或“0”）
- **limit-bytes-in** - 发送的字节限制（“1000000”或“---”如果没有限制）
- **limit-bytes-out** - 接收字节限制（“1000000”或“---”如果没有限制）
- **refresh-timeout** - 状态页面刷新超时（“1m30s”或“”）
- **refresh-timeout-secs** - 状态页面刷新超时秒数（“90s”或“0”）
- **session-timeout** - 用户的会话时间（如果没有则为“5h”或“”）
- **session-timeout-secs** - 用户的会话时间，以秒为单位（如果超时则为“3475”或“0”）
- **session-time-left** -用户的会话时间（如果没有则为“5h”或“”）
- **session-time-left-secs** - 用户的会话时间，以秒为单位（如果超时则为“3475”或“0”）
- **uptime** - 当前会话正常运行时间（“10h2m33s”）
- **uptime-secs** - 当前会话正常运行时间（以秒为单位）（“125”）

**流量计数器，仅在状态页面中可用：**

- **bytes-in** - 从用户接收到的字节数（“15423”）
- **bytes-in-nice** - 用户友好的字节数形式（“15423”）
- **bytes-out** - 发送给用户的字节数（“11352”）
- **bytes-out-nice** - 发送给用户的字节数的用户友好形式（“11352”）
- **packets-in** - 从用户收到的数据包数量（“251”）
- **packets-out** - 发送给用户的数据包数量（“211”）
- **remain-bytes-in** - 达到 limit-bytes-in 之前的剩余字节数（如果没有限制，则为“337465”或“---”）
- **remain-bytes-out** - 达到 limit-bytes-out 之前的剩余字节数（如果没有限制，则为“124455”或“---”）

**其他变量：**

- **session-id** - 上次请求中“session-id”参数的值
- **var** - 上次请求中“var”参数的值
- **error** - 错误消息，如果出现问题（“无效的用户名或密码”）
- **error-orig** - 原始错误消息（没有从 errors.txt 中检索的翻译），如果出现问题（“无效的用户名或密码”）
- **chap-id** - chap ID 的值 ("\\371")
- **chap-challenge** - chap 挑战值 ("\\357\\015\\330\\013\\021\\234\\145\\245\\303\\253\\142\\ 246\\133\\175\\375\\316")
- **popup** - 是否弹出复选框（“true”或“false”）
- **advert-pending** - 通告是否待显示（“是”或“否”）
- **http-status** - 允许设置 http 状态代码和消息
- **http-header** - 允许设置 http 标头

**RADIUS 相关变量：**

- **radius<id>** - 以文本字符串形式显示用 <id> 标识的属性（如果使用 RADIUS 身份验证；否则为“”）
- **radius<id>u** - 以无符号整数形式显示用 <id> 标识的属性（如果使用 RADIUS 身份验证；否则为“0”）
- **radius<id>-<vnd-id>** - 以文本字符串形式显示用 <id> 和供应商 ID <vnd-id> 标识的属性（如果使用 RADIUS 身份验证；否则为“”）
- **radius<id>-<vnd-id>u** - 以无符号整数形式显示用 <id> 和供应商 ID <vnd-id> 标识的属性（如果使用 RADIUS 身份验证；否则为“0”）

#### 使用变量

\$(if <var_name>) 语句可以在这些页面中使用。 如果 <var_name> 的值不是空字符串，则将包含以下内容。 它等价于 \$(if <var_name> != "") 也可以进行等价比较： \$(if <var_name> == <value>) 这些语句在 \$(elif <var_name>)、\$(else) 或 \$(endif)。 在一般情况下，它看起来像这样：

```shell
some content, which will always be displayed
$(if username == john)
Hey, your username is john
$(elif username == dizzy)
Hello, Dizzy! How are you? Your administrator.
$(elif ip == 10.1.2.3)
You are sitting at that crappy computer, which is damn slow...
$(elif mac == 00:01:02:03:04:05)
This is an ethernet card, which was stolen few months ago...
$(else)
I don't know who you are, so lets live in peace.
$(endif)
other content, which will always be displayed

```

只显示其中一个表达式。 取决于每个客户的这些变量的值。

#### 重定向和自定义标头

```shell
$(if http-status == 302)Hotspot login required$(endif)
$(if http-header == "Location")$(link-redirect)$(endif)

```

**注意：** 虽然上面使用了条件表达式“if”，但实际上是将“http-status”设置为“302”而不是对其进行测试。 变量“http-header”也是如此。 即使它使用“if”，它实际上是将变量设置为“Location”，然后从变量“link-redirect”设置的 url。

例如。 在 \$(link-redirect) 评估为“[http://192.168.88.1/login](http://192.168.88.1/login)”的情况下，返回给客户端的 HTTP 响应将更改为：

```
HTTP/1.0 302 Hotspot login required
<regular HTTP headers>
Location: http://192.168.88.1/login

```
  
**http-status 语法**:

```
$(if http-status == XYZ)HTTP_STATUS_MESSAGE$(endif)

```

- _XYZ_ - 希望返回的状态代码。 应该是3个十进制数字，第一个不能是0
- _HTTP\_STATUS\_MESSAGE_ - 希望返回给客户端的任何文本，这些文本将遵循 HTTP 回复中的上述状态代码

在任何 HTTP 响应中，它将位于第一行，如下所示：

```
HTTP/1.0 XYZ HTTP_STATUS_MESSAGE

```
  
**http-header syntax:**

```
$(if http-header == HTTP_HEADER_NAME)HTTP_HEADER_VALUE$(endif)

```

- _HTTP\_HEADER\_NAME_ - 要在响应中发送的 HTTP 标头的名称
- _HTTP\_HEADER\_VALUE_ - 要在响应中发送的名为 HTTP\_HEADER\_NAME 的 HTTP 标头的值

HTTP 响应将显示为：

```
HTTP_HEADER_NAME: HTTP_HEADER_VALUE

```
  
HTTP\_HEADER\_VALUE 和 HTTP\_STATUS\_MESSAGE 中的所有变量和条件表达式都照常处理。

如果添加了多个具有相同名称的标头，则只会使用最后一个标头（将丢弃之前的标头）。 它允许系统覆盖常规 HTTP 标头（例如，Content-Type 和 Cache-Control）。

### 自定义错误消息

所有错误消息都存储在相应 HotSpot servlet 目录中的 errors.txt 文件中。 你可以将所有这些消息更改并翻译成你的母语。 为此，请编辑 errors.txt 文件。 你还可以在消息中使用变量。 所有说明都在该文件中给出。

### 多个版本的 HotSpot 页面

支持同一 HotSpot 服务器的多个 HotSpot 页面集。 它们可以由用户选择（选择语言）或由 JavaScript 自动选择（选择 PDA/HTML 页面的常规版本）。

要利用此功能，请在 HotSpot HTML 目录中创建子目录，并将那些不同的 HTML 文件放在该子目录中。 例如，要翻译拉脱维亚语的所有内容，可以创建子目录“lv”，其中包含翻译成拉脱维亚语的 login.html、logout.html、status.html、alogin.html、radvert.html 和 errors.txt 文件。 如果在请求的子目录中找不到请求的 HTML 页面，将使用主目录中相应的 HTML 文件。 然后主 login.html 文件将包含指向“/lv/login?dst=\$(link-orig-esc)”的链接，然后显示拉脱维亚版本的登录页面：<a href="/lv/login?dst=\$ (link-orig-esc)">拉脱维亚语</a> . 拉脱维亚版本将包含指向英文版本的链接：<a href="/login?dst=$(link-orig-esc)">English</a>

引用目录的另一种方法是指定“目标”变量：

```
        <a href="$(link-login-only)?dst=$(link-orig-esc)&target=lv">Latviski</a>
        <a href="$(link-login-only)?dst=$(link-orig-esc)&target=%2F">English</a>

```

选择首选目录后（例如，“lv”），所有指向本地 HotSpot 页面的链接都将包含该路径（例如，\$(link-status) = [http://hotspot.mt.lv/lv/status](http://hotspot.mt.lv/lv/status) 。 因此，如果所有 HotSpot 页面都使用“$(link-xxx)”变量引用链接，则不再需要进行任何更改 - 每个客户端将一直停留在所选目录中。

### 杂项

如果你想使用 HTTP-CHAP 身份验证方法，则应该在 **提交** 之前包含 **doLogin()** 函数（它引用必须已经加载的 **md5.js**） 登录表单的操作。 否则，CHAP 登录将失败。

在 HTTP-CHAP 方法的情况下，要发送到 HotSpot 网关的结果密码由以下内容的 MD5 散列连接组成：chap-id、用户密码和 chap-challenge（按给定顺序）

如果要直接在链接中使用变量，则必须相应地对它们进行转义。 例如，登录页面 **\<a href="https://login.example.com/login?mac=\$(mac)&user=\$(username)"\>link\</a\>** 如果用户名是“123\&456=1 2”，不会 按预期工作。 因此，必须使用其转义版本而不是 \$(user)：\$(user-esc): **\<a href="https://login.server.serv/login?mac=\$(mac-esc )\&user=\$(user-esc)"\>link\</a\>**。 现在相同的用户名将转换为“123%26456%3D1+2”，这是 URL 中“123&456=1 2”的有效表示。 这个技巧可以用于任何变量，而不仅仅是 $(username)。

注销页面有一个布尔参数“erase-cookie”，它可以是“on”或“true”以在注销时删除用户cookie(这样用户在打开浏览器时就不会自动登录)。

### 例子

有了基本的 HTML 语言知识和下面的例子，应该很容易实现上面描述的想法。

- 要提供预定义值作为用户名，请在 login.html 中更改：

```html
<type="text" value="$(username)>

```

到此行:

```html
<input type="hidden" name="username" value="hsuser">

```

（其中 hsuser 是你提供的用户名）

- 要提供预定义值作为密码，请在 login.html 中更改：

```html
<input type="password">

```

到此行:

```html
<input type="hidden" name="password" value="hspass">

```

（其中 hspass 是你提供的密码）

- 以下形式将客户端的 MAC 地址发送到注册服务器：

[https://www.example.com/register.html?mac=XX:XX:XX:XX:XX:XX](https://www.example.com/register.html?mac=XX:XX:XX:XX:XX:XX)

将 login.html 中的登录按钮链接更改为：

```html
https://www.example.com/register.html?mac=$(mac)

```

（应该修改链接指向你的服务器）

- 在用户登录后显示横幅，在 alogin.html 之后

\$(if popup == 'true') add the following line:

```html
open('http://www.example.com/your-banner-page.html', 'my-banner-name','');

```

（应该修改链接指向你要显示的页面）

- 要选择登录后显示的不同页面，请在 login.html 中更改：

```html
<input type="hidden" name="dst" value="$(link-orig)">

```

到此行:

```html
<input type="hidden" name="dst" value="http://www.example.com">

```

（应该修改链接指向你的服务器）

- 要在注销时删除 cookie，请在包含注销链接的页面（例如，在 status.html 中）更改：

```html
open('$(link-logout)', 'hotspot_logout', ...

```

到这里:

```html
open('$(link-logout)?erase-cookie=on', 'hotspot_logout', ...

```

或者添加这一行：

```html
<input type="hidden" name="erase-cookie" value="on">

```

在此之前:

```html
<input type="submit" value="log off">

```

外部认证 [Edit](https://wiki.mikrotik.com/index.php?title=Manual:Customizing_Hotspot&action=edit&section=13)

另一个例子是让 HotSpot 在远程服务器上进行身份验证（例如，可以执行信用卡收费）：

- 允许直接访问围墙花园中的外部服务器（基于 HTTP 或基于 IP）
- 修改 HotSpot servlet 的登录页面以重定向到外部认证服务器。 外部服务器应根据需要修改 RADIUS 数据库

这是放置在HotSpot路由器上的此类登录页面的示例,重定向到 [https://auth.example.com/login.php](https://auth.example.com/login.php) ，替换为外部认证服务器的实际地址）：

```html
<html>
<title>...</title>
<body>
<form name="redirect" action="https://auth.example.com/login.php" method="post">
<input type="hidden" name="mac" value="$(mac)">
<input type="hidden" name="ip" value="$(ip)">
<input type="hidden" name="username" value="$(username)">
<input type="hidden" name="link-login" value="$(link-login)">
<input type="hidden" name="link-orig" value="$(link-orig)">
<input type="hidden" name="error" value="$(error)">
</form>
<script language="JavaScript">
<!--
document.redirect.submit();
//-->
</script>
</body>
</html>
          

```

- 外部服务器可以通过将 HotSpot 客户端重定向回原始 HotSpot servlet 登录页面并指定正确的用户名和密码来登录 HotSpot 客户端

下面是一个页面的示例,重定向到 [https://hotspot.example.com/login](https://hotspot.example.com/login) ，替换为HotSpot路由器的实际地址； 此外，成功登录后显示 [www.mikrotik.com](http://www.mikrotik.com/) ，替换为需要的内容：

```html
<html>
<title>Hotspot login page</title>
<body>
<form name="login" action="https://hotspot.example.com/login" method="post">
<input type="text" name="username" value="demo">
<input type="password" name="password" value="none">
<input type="hidden" name="domain" value="">
<input type="hidden" name="dst" value="http://www.mikrotik.com/">
<input type="submit" name="login" value="log in">
</form>
</body>
</html>
          

```

- Hotspot 会询问 RADIUS 服务器是否允许登录。 如果允许，将显示 alogin.html 页面（可以对其进行修改以执行任何操作）。 如果不允许，将显示 flogin.html（或 login.html）页面，这会将客户端重定向回外部认证服务器。

**注意：** 如这些示例所示，HTTPS 协议和 POST 方法可用于保护通信。

Hotspot 登录页面可以使用 **$(http-header-name);** 访问 HTTP 标头

例如，存在检查用户代理（或浏览器）的能力，如果需要，将返回任何其他内容而不是常规登录页面。 例如，这可用于禁用手机中的自动弹出窗口。

例如，要为特定 Firefox 移动版本的用户输出“SUCCESS”，而不是登录页面，你可以在热点目录中的 **rlogin.html** 页面顶部添加以下行：

```html
$(if user-agent == "Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0" ) 
<HTML><HEAD><TITLE>Success</TITLE></HEAD><BODY>Success</BODY></HTML> 
$(else)
---- regular content of rlogin.html page  ----
$(endif)

```

这将禁用 Android Firefox 40 用户的登录弹出窗口。

#### 一键登录

在不需要用户或密码的情况下，可以创建修改后的强制门户以实现快速一键登录。

你需要做的是：

- 为此创建用户。 例如，它是“notsosecretuser”，密码为“notsosecretpass”
- 将此用户分配给允许特定/无限数量的同时活动用户的用户配置文件。
- 复制已在根级别的路由器文件菜单中生成的原始热点目录。
- 修改此副本目录内容的内容。
  - 只有一个文件需要修改-login.html。

原始内容：

```html
<table width="100" style="background-color: #ffffff">
  <tr><td align="right">login</td>
      <td><input style="width: 80px" name="username" type="text" value="$(username)"/></td>
  </tr>
  <tr><td align="right">password</td>
      <td><input style="width: 80px" name="password" type="password"/></td>
  </tr>
  <tr><td> </td>
      <td><input type="submit" value="OK" /></td>
  </tr>
</table>

```

修改为:

```html
<table width="100" style="background-color: #ffffff">
  <tr style="display:none;"><td align="right">login</td>
    <td><input style="width: 80px" name="username" type="text" value="notsosecretuser"/></td>
  </tr>
  <tr style="display:none;"><td align="right">password</td>
    <td><input style="width: 80px" name="password" type="password" value="notsosecretpass"/></td>
  </tr>
  <tr><td> </td>
    <td><input type="submit" value="Proceed to Internet!" /></td>
  </tr>
</table>

```

发生了什么：

- 用户和密码“”字段被隐藏。
- 用户和密码字段值都包含预定义值。
- 将“确定”按钮值（名称）更改为更合适的值。

- 现在将这个新的hotspot文件夹上传回路由器，最好使用不同的名称。
- 更改热点服务器配置文件中的设置以使用这个新的 html 目录。

```shell
/ip hotspot profile set (profile number or name) html-directory-override=(dir path/name)

```

## 防火墙自定义

### 概述

除了 /ip hotspotSubmenu中明显的动态条目（如主机和活动用户）之外，在激活 HotSpot 服务时，还会在防火墙表中添加一些额外的规则。

### NAT

从 **/ip firewall nat print dynamic** 命令，你可以得到（每条规则后面都有注释）：

```
 0 D chain=dstnat action=jump jump-target=hotspot hotspot=from-client

```

将来自所有 HotSpot 客户端的数据包的所有 HotSpot 相关任务放入一个单独的链中。

```
 1 I chain=hotspot action=jump jump-target=pre-hotspot

```

任何应该在 HotSpot 规则应用之前完成的操作，都应该放在预热点链中。 该链完全由管理员控制，不包含系统设置的任何规则，因此跳转规则无效（因为该链默认没有任何规则）。

```
 2 D chain=hotspot action=redirect to-ports=64872 dst-port=53 protocol=udp 
 3 D chain=hotspot action=redirect to-ports=64872 dst-port=53 protocol=tcp 

```

将所有 DNS 请求重定向到 HotSpot 服务。 64872端口为所有HotSpot用户提供DNS服务。 如果你希望 HotSpot 服务器也监听另一个端口，请以相同的方式在此处添加规则，更改 dst-port 属性。

```
 4 D chain=hotspot action=redirect to-ports=64873 hotspot=local-dst dst-port=80
     protocol=tcp

```

将所有 HTTP 登录请求重定向到 HTTP 登录 servlet。 64873 是 HotSpot HTTP servlet 端口。

```
 5 D chain=hotspot action=redirect to-ports=64875 hotspot=local-dst dst-port=443
     protocol=tcp

```

将所有 HTTPS 登录请求重定向到 HTTPS 登录 servlet。 64875 是 HotSpot HTTPS servlet 端口。

```
 6 D chain=hotspot action=jump jump-target=hs-unauth hotspot=!auth protocol=tcp

```

除 DNS 和来自未授权客户端的登录请求外，所有其他数据包都应通过 hs-unauth 链。

```
 7 D chain=hotspot action=jump jump-target=hs-auth hotspot=auth protocol=tcp

```

来自授权客户端的数据包 - 通过 hs-auth 链。

```
 8 D ;;; www.mikrotik.com
     chain=hs-unauth action=return dst-address=66.228.113.26 dst-port=80 protocol=tcp

```

在 **hs-unauth** 链中，首先将影响 TCP 协议的所有内容放入 `/ip hotspot walled-garden ip` Submenu中（即，未设置协议或设置为 TCP 的所有内容）。 这里将 [www.mikrotik.com](http://www.mikrotik.com/) 排除在重定向到登录页面之外。

```
 9 D chain=hs-unauth action=redirect to-ports=64874 dst-port=80 protocol=tcp

```

所有其他 HTTP 请求都被重定向到监听 64874 端口的 Walled Garden 代理服务器。 如果 HTTP 请求的 /ip hotspot walled-garden 菜单中有一个允许条目，则该请求将被转发到目的地。 否则，请求将自动重定向到 HotSpot 登录 servlet（端口 64873）。

```
10 D chain=hs-unauth action=redirect to-ports=64874 dst-port=3128 protocol=tcp 
11 D chain=hs-unauth action=redirect to-ports=64874 dst-port=8080 protocol=tcp 

```

HotSpot 默认假定只有这些端口可用于 HTTP 代理请求。 这两个条目用于“捕获”客户端对未知代理的请求（你可以在此处为其他端口添加更多规则）。 即使有未知代理设置的客户端可以使用 HotSpot 系统。 此功能称为“通用代理”。 如果检测到客户端正在使用某个代理服务器，系统会自动用 http 热点标记标记该数据包以解决未知代理问题，我们将在后面看到。 请注意，使用的端口 (64874) 与规则 #9 中的 HTTP 请求相同（因此 HTTP 和 HTTP 代理请求都由相同的代码处理）。

```
12 D chain=hs-unauth action=redirect to-ports=64875 dst-port=443 protocol=tcp

```

HTTPS 代理监听64875端口.

```
13 I chain=hs-unauth action=jump jump-target=hs-smtp dst-port=25 protocol=tcp

```

也可以在 HotSpot 配置中定义 SMTP 协议的重定向。 如果是，重定向规则将被放入 hs-smtp 链中。 这样做是为了让具有未知 SMTP 配置的用户能够通过服务提供商的（你的）SMTP 服务器发送邮件，而不是转到用户在其计算机上配置的[possibly unavailable outside their network of origin] SMTP 服务器 . 默认情况下链为空，因此跳转规则无效。

```
14 D chain=hs-auth action=redirect to-ports=64874 hotspot=http protocol=tcp

```

为授权用户提供HTTP代理服务。 经过身份验证的用户请求可能需要接受透明代理（“通用代理”技术和通告功能）。 此 http 标记自动放置在 HotSpot HTTP 代理（侦听 64874 端口的代理）检测到的服务器的 HTTP 代理请求上，作为对未知代理服务器的 HTTP 代理请求。 这样做是为了让具有某些代理设置的用户可以使用 HotSpot 网关，而不是用户在其计算机中配置的 **可能在其原始网络之外不可用** 代理服务器。 如果通告应该显示给用户，以及从配置文件配置为透明代理其请求的用户发出的任何 HTTP 请求上，也会应用此标记。

```
15 I chain=hs-auth action=jump jump-target=hs-smtp dst-port=25 protocol=tcp

```

为授权用户提供 SMTP 代理（与规则 #13 相同）。

### 数据包过滤

从 **/ip firewall filter print dynamic** 命令，你可以得到（注释跟在每条规则之后）：

```
 0 D chain=forward action=jump jump-target=hs-unauth hotspot=from-client,!auth

```

任何从未经授权的客户端穿过路由器的数据包都将被发送到 **hs-unauth** 链。 hs-unauth 实现了基于 IP 的 Walled Garden 过滤器。

```
 1 D chain=forward action=jump jump-target=hs-unauth-to hotspot=to-client,!auth

```

通过路由器到达客户端的所有内容都被重定向到另一个链，称为 **hs-unauth-to**。 该链应拒绝对客户端未经授权的请求。

```
 2 D chain=input action=jump jump-target=hs-input hotspot=from-client

```

从客户端到路由器本身的所有内容都会到达另一个链，称为 **hs-input**。

```
 3 I chain=hs-input action=jump jump-target=pre-hs-input

```

在继续执行[predefined] 动态规则之前，数据包到达管理控制的 **pre-hs-input** 链，默认情况下该链为空，因此跳转规则处于无效状态。

```
 4 D chain=hs-input action=accept dst-port=64872 protocol=udp 
 5 D chain=hs-input action=accept dst-port=64872-64875 protocol=tcp 

```

允许客户端访问本地身份验证和代理服务（如前所述）。

```
 6 D chain=hs-input action=jump jump-target=hs-unauth hotspot=!auth

```

从未经授权的客户端到路由器本身的所有其他流量将被视为和穿越路由器的流量相同的方式。

```
 7 D chain=hs-unauth action=return protocol=icmp
 8 D ;;; www.mikrotik.com
     chain=hs-unauth action=return dst-address=66.228.113.26 dst-port=80 protocol=tcp

```

与仅添加与 TCP 协议相关的 Walled Garden 条目的 NAT 表不同，在数据包过滤器 **hs-unauth** 链中添加了在 **/ip hotspot walled-garden ip** 菜单中设置的所有内容。 这就是为什么尽管在 NAT 表中只看到一个条目，但这里有两条规则。

```
 9 D chain=hs-unauth action=reject reject-with=tcp-reset protocol=tcp
10 D chain=hs-unauth action=reject reject-with=icmp-net-prohibited

```

围墙花园未列出的所有其他内容都将被拒绝。 注意使用 TCP Reset 来拒绝 TCP 连接。

```
11 D chain=hs-unauth-to action=return protocol=icmp
12 D ;;; www.mikrotik.com
     chain=hs-unauth-to action=return src-address=66.228.113.26 src-port=80 protocol=tcp

```

对于发往客户端（链 **hs-unauth-to**）的数据包，也执行与规则 #7 和 #8 中相同的操作。

```
13 D chain=hs-unauth-to action=reject reject-with=icmp-host-prohibited

```

使用 ICMP 拒绝消息拒绝所有发往客户端的数据包。