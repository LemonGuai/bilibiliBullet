--b站弹幕表 '@auther:lemon;@createdate:2020.05.24'
CREATE TABLE t_bilili_video_bullet
(  
  id int NOT NULL primary key AUTO_INCREMENT,
  BVcode      varchar(20),
  cid         varchar(10),
  text        TEXT,
  sender      nvarchar(50),
  senddate    DATETIME,
  operator    nvarchar(50),
  optiondate  DATETIME
);
--免费代理IP表  '@auther:lemon;@createdate:2020.06.28'
CREATE TABLE t_free_agent_IP_test
(
  id int NOT NULL primary key AUTO_INCREMENT,
  IP          varchar(15),
  Port        varchar(10),
  Type        varchar(5),
  Anonymous    varchar(10),
  Response    varchar(10)),
  isvalid     int(1),           -- 1 有效; 2 无效
  usenum      int(10),
  location    varchar(100),
  validtime   DATETIME,
  optiondate  DATETIME
);