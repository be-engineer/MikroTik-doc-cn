下面文章解释了如何使用RouterOS的GPS功能和脚本来创建一个简单的车辆跟踪系统。

# 方法

这种方法使用RouterOS Fetch工具的HTTP POST功能。允许你从RouterOS命令行向网络服务器发送任何类型的数据。可以使用脚本，用变量来填充POST数据。发布的数据写入一个SQLITE3数据库（如果文件不存在会自动创建），然后，从数据库中读取，并将其加入Leaflet.js的PolyLine数组。这是一个概念验证的例子，没有认证、安全或错误处理。

# 要求

- 选择的网络服务器
- PHP
- PHP的SQLite3模块
- 带有工作的GPS模块的RouterOS设备
- RouterOS v6.40rc30或以上版本
- 在RouterOS中设置GPS格式为 **dd**。

# RouterOS脚本

可以在Scheduler工具中运行这个脚本，间隔时间为1s，让坐标每1秒发送一次。

```shell
{
:global lat
:global lon
/system gps monitor once do={
:set $lat $("latitude")
:set $lon $("longitude")
}
tool fetch mode=http url="http://YOURSERVER.com/index.php" port=80 http-method=post http-data=("{\"lat\":\"" . $lat . "\",\"lon\":\"" . $lon . "\"}") http-header-field="Content-Type: application/json"
:put ("{\"lat\":\"" . $lat . "\",\"lon\":\"" . $lon . "\"}")
}
```

# index.php文件

在index.php文件旁边创建一个名为 **sqlite_db** 的空目录。用 **chmod -R a+w sqlite_db/** 确保该目录和文件可以写入。

```php
<?php
$loc = dirname(__FILE__).'/sqlite_db/coord.db';
$db = new SQLite3($loc,SQLITE3_OPEN_READWRITE | SQLITE3_OPEN_CREATE);
$raw = file_get_contents('php://input');
$raw = preg_replace('/\\x00/','',$raw);
$data = json_decode($raw);
 
if (!empty($data) && is_object($data) && property_exists($data,'lat') && property_exists($data,'lon')){
    if(file_exists($loc)) echo 'exists!'.chr(0xa);
    $src = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'coordinates\'';
    $res = $db->querySingle($src);
    if (count($res)==0){
            $db->exec('CREATE TABLE coordinates (latitude TEXT, longitude TEXT, time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, added TIMESTAMP DEFAULT CURRENT_TIMESTAMP ) ');
    }
     
$regex = '/^(|\-)([0-9]{2,3}\.[0-9]{0,8})$/';
 
if (preg_match($regex,$data->lat) && preg_match($regex,$data->lon) )
    {
        $lat = $data->lat;
        $lon = $data->lon;
    }
    $ins = 'INSERT INTO coordinates (latitude,longitude) VALUES (\''.SQLite3::escapeString($lat).'\',\''.SQLite3::escapeString($lon).'\')';
    $db->exec($ins);
    die();
}
?>
 
<!DOCTYPE html>
<html>
<head>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.3.1/dist/leaflet.css" integrity="sha512-Rksm5RenBEKSKFjgI3a41vrjkw4EVPlJ3+OiI65vTjIdo9brlAacEuKOiQ5OFh7cOI1bkDwLqdLw3Zg0cRJAAQ==" crossorigin=""/>
  <script src="https://unpkg.com/leaflet@1.3.1/dist/leaflet.js" integrity="sha512-/Nsx9X4HebavoBvEBuyp3I7od5tA0UzAxs+j83KgC8PU0kgB4XiK4Lfe4y4cgBtaRJQEIFCW+oC506aPT2L1zw==" crossorigin=""></script>
</head>
<body>
<div id="map" style="width: 800px; height: 600px;"></div>
<script>
var map = L.map('map').setView([0,0], 4);
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {attribution: '<a href="http://osm.org/copyright">OSM</a>'}).addTo(map);
 
<?php
    if($result = $db->query('SELECT latitude,longitude FROM coordinates')){
    echo ' var latlngs = [ ';
    while($obj = $result->fetchArray()){
        if (!is_array($obj) || !isset($obj['latitude']) || !isset($obj['longitude']) || empty($obj['latitude']) || empty($obj['longitude'])) continue;
        echo '["'. $obj['latitude'].'","'.$obj['longitude'].'"],';
    }
    echo ']; ';
    } else
     echo('//'.$db->lastErrorMsg().chr(0xa)); 
     echo($data);
?>
var polyline = L.polyline(latlngs, {color: 'red'}).addTo(map);
map.fitBounds(polyline.getBounds());
</script>
</body>
</html>
```

# 结果

![](https://help.mikrotik.com/docs/download/attachments/84901903/image2021-9-7_12-41-40.png?version=1&modificationDate=1631007699790&api=v2)