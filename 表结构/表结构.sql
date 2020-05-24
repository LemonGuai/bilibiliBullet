--b站弹幕表 '@auther:lemon;@createdate:2020.05.24'
CREATE TABLE `t_bilili_video_bullet`(  
  `id` int NOT NULL primary key AUTO_INCREMENT,
  `BVcode`      varchar(20),
  `cid`         varchar(10),
  `text`        TEXT,
  `sender`      nvarchar(50),
  `senddate`    DATETIME,
  `operator`    nvarchar(50),
  `optiondate`  DATETIME
);
