insert into t_free_agent_ip_test(IP,Port,Type,Anonymous,Response,isvalid,usenum,location,validtime,optiondate)
select  %s, %s, %s, %s, %s, 0, 0, %s, %s, %s
;