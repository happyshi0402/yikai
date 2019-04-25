#!/usr/bin/env bash

type=$1
port=$2
task_name=$3
screen_name="ngrok_zkhc_${task_name}"
ali_port=$((port+10000))
ngrok_port=$((port+6000))
echo ${ali_port}, ${ngrok_port}
PID=$(screen -ls|grep "${screen_name}"|grep -v gref | awk '{ print $2 }')
echo $PID
if [[ "$PID" =~ "(Detached)" ]];
then
    echo "screen Detached ${screen_name} is exist"
elif [[ "$PID" =~ "(Attached)" ]];
then
    echo "screen Attached ${screen_name} is exist"
else
    screen -dmS ${screen_name}
fi

if [[ ${type} =~ "http" ]] ;
then
    echo "${type}  action"
    cat > /home/zkhc_wsf/zkhc_monitor/ngrok/ngrok/ngrok.${task_name}.yml <<EOF
server_addr: ngrok.kangmochou.com:4443
trust_host_root_certs: false
tunnels:
  ${task_name}:
    proto:
      ${type}: ${port}
EOF
    echo "create ngrok yml success"
    screen -x -S $screen_name -p 0 -X stuff \
    "cd /home/zkhc_wsf/zkhc_monitor/ngrok/ngrok/\n./bin/ngrok -config=ngrok.${task_name}.yml start ${task_name}\n"

elif [ ${type} == "tcp" ] ;
then
    # todo tcp 协议处理
    # 需要额外产生nginx文件
    echo "tcp  action"

    cat > /home/zkhc_wsf/zkhc_monitor/ngrok/ngrok/ngrok.${task_name}.yml <<EOF
server_addr: ngrok.kangmochou.com:4443
trust_host_root_certs: false
tunnels:
  ${task_name}:
    remote_port: ${ngrok_port}
    proto:
      ${type}: ${port}
EOF
    echo "create ngrok yml success"
    screen -x -S $screen_name -p 0 -X stuff \
    "cd /home/zkhc_wsf/zkhc_monitor/ngrok/ngrok/\n./bin/ngrok -config=ngrok.${task_name}.yml start ${task_name}\n"


    cat > /home/zkhc_wsf/zkhc_monitor/aliyun/etc/nginx/conf.tcp.d/nginx.${task_name}.conf <<EOF
server {
    # for ${task_name}
    listen ${ali_port};
    proxy_pass 172.17.92.158:${ngrok_port};
}
EOF
    scp /home/zkhc_wsf/zkhc_monitor/aliyun/etc/nginx/conf.tcp.d/nginx.${task_name}.conf root@47.94.204.122:/etc/nginx/conf.tcp.d/
    ssh root@47.94.204.122 << remotessh
ps -ef | grep nginx
exec ps -ef | grep nginx | grep -v grep | awk '{print $2}'| xargs kill -9
ps -ef | grep nginx
nginx
ps -ef | grep nginx
exit
remotessh
else
   echo "没有符合的条件"
fi

# sh set_ngrok.sh tcp 22 ssh
# sh set_ngrok.sh http 508 admin_dev