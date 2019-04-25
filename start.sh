#!/usr/bin/env bash

#!/bin/sh
# name:start_web
# start web

base_path=/home/zkhc_wsf/zkhc_webhook/
soft_path=${base_path}
web_path=${base_path}
log_path=${base_path}/logs
web_soft_name=manage
log_name=zkhc_webhook_log
web_port=1571

for port in ${web_port}
do
    lsof -i:$port | awk '{print $2}' | tail -n +2| while read id
    do
            kill -9 $id
    done
done
echo "kill old system"

cd ${base_path}
today=`date +%Y-%m-%d`
echo "restart new code"ls
echo "nohup /home/zkhc_wsf/zkhc_wsf_env/bin/gunicorn --chdir ${web_path} -w 4 -k gevent -b 0.0.0.0:${web_port} ${web_soft_name}:app 1>> ${log_path}/${today}_${log_name}.log 2>> ${log_path}/${today}_${log_name}_error.log&"

nohup /home/zkhc_wsf/zkhc_wsf_env/bin/gunicorn --chdir ${web_path} -w 4 -k gevent -b 0.0.0.0:${web_port} ${web_soft_name}:app 1>> ${log_path}/${today}_${log_name}_error.log 2>> ${log_path}/${today}_${log_name}.log&
echo $! >> service.pid
echo "restart code over"


#cat ${log_path}/${today}_${log_name}_error.log
lsof -i:${web_port}