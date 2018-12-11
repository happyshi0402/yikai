#!/usr/bin/env bash

NGINX_VERSION=1.15.7
GPG_KEYS=B0F4253373F8F6F510D42178520A9993A1C052F8
CONFIG="\
		--prefix=/etc/nginx \
		--with-ld-opt=-Wl,-rpath,/usr/local/luajit/lib \
        --add-module=/usr/local/ngx_devel_kit \
        --add-module=/usr/local/lua-nginx-module \
		--sbin-path=/usr/sbin/nginx \
		--modules-path=/usr/lib/nginx/modules \
		--conf-path=/etc/nginx/nginx.conf \
		--error-log-path=/var/log/nginx/error.log \
		--http-log-path=/var/log/nginx/access.log \
		--pid-path=/var/run/nginx.pid \
		--lock-path=/var/run/nginx.lock \
		--http-client-body-temp-path=/var/cache/nginx/client_temp \
		--http-proxy-temp-path=/var/cache/nginx/proxy_temp \
		--http-fastcgi-temp-path=/var/cache/nginx/fastcgi_temp \
		--http-uwsgi-temp-path=/var/cache/nginx/uwsgi_temp \
		--http-scgi-temp-path=/var/cache/nginx/scgi_temp \
		--user=nginx \
		--group=nginx \
		--with-http_ssl_module \
		--with-http_realip_module \
		--with-http_addition_module \
		--with-http_sub_module \
		--with-http_dav_module \
		--with-http_flv_module \
		--with-http_mp4_module \
		--with-http_gunzip_module \
		--with-http_gzip_static_module \
		--with-http_random_index_module \
		--with-http_secure_link_module \
		--with-http_stub_status_module \
		--with-http_auth_request_module \
		--with-http_xslt_module=dynamic \
		--with-http_image_filter_module=dynamic \
		--with-http_geoip_module=dynamic \
		--with-threads \
		--with-stream \
		--with-stream_ssl_module \
		--with-stream_ssl_preread_module \
		--with-stream_realip_module \
		--with-stream_geoip_module=dynamic \
		--with-http_slice_module \
		--with-mail \
		--with-mail_ssl_module \
		--with-compat \
		--with-file-aio \
		--with-http_v2_module \
	"
groupadd nginx
useradd -s /sbin/nologin -M -g nginx nginx
yum install -y gcc \
	libc-dev \
	make \
	zlib-dev \
	linux-headers \
	curl \
	gnupg1 \
	libxslt-dev \
	gd-dev \
	geoip-dev \
	libxml2 libxml2-dev \
	libxslt-devel \
	gd-devel \
	GeoIP GeoIP-devel GeoIP-data \
	pcre pcre-devel \
	openssl openssl-devel

cd /usr/local/src

curl -fSL https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz -o nginx.tar.gz
curl -fSL https://nginx.org/download/nginx-$NGINX_VERSION.tar.gz.asc  -o nginx.tar.gz.asc
curl -fSL http://luajit.org/download/LuaJIT-2.0.5.tar.gz -o LuaJIT-2.0.5.tar.gz
#wget -c http://luajit.org/download/LuaJIT-2.0.5.tar.gz
tar xzvf LuaJIT-2.0.5.tar.gz
cd LuaJIT-2.0.5
make install PREFIX=/usr/local/luajit
export LUAJIT_LIB=/usr/local/luajit/lib
export LUAJIT_INC=/usr/local/luajit/include/luajit-2.0

curl -fSL https://github.com/simpl/ngx_devel_kit/archive/v0.3.0.tar.gz -o ngx_devel_kit.v0.3.0.tar.gz
#wget https://github.com/simpl/ngx_devel_kit/archive/v0.3.0.tar.gz
tar -xzvf ngx_devel_kit.v0.3.0.tar.gz
mv ngx_devel_kit-0.3.0 ngx_devel_kit
cp -rf ngx_devel_kit /usr/local
#https://codeload.github.com/openresty/lua-nginx-module/tar.gz/v0.10.11rc2
#https://codeload.github.com/openresty/lua-nginx-module/tar.gz/v0.10.14rc3
curl -fSL  https://github.com/openresty/lua-nginx-module/archive/v0.10.13.tar.gz -o lua-nginx-module.v0.10.13.tar.gz
#wget https://github.com/openresty/lua-nginx-module/archive/v0.10.13.tar.gz
tar -xzvf lua-nginx-module.v0.10.13.tar.gz
mv lua-nginx-module-0.10.13 lua-nginx-module
cp -rf lua-nginx-module /usr/local

export GNUPGHOME="$(mktemp -d)"
found=''
    for server in \
        ha.pool.sks-keyservers.net \
        hkp://keyserver.ubuntu.com:80 \
        hkp://p80.pool.sks-keyservers.net:80 \
        pgp.mit.edu;
        do
        echo "Fetching GPG key $GPG_KEYS from $server"
        gpg --keyserver "$server" --keyserver-options timeout=10 --recv-keys "$GPG_KEYS" && found=yes && break;
    done;
    test -z "$found" && echo >&2 "error: failed to fetch GPG key $GPG_KEYS" && exit 1;
    gpg --batch --verify nginx.tar.gz.asc nginx.tar.gz
rm -rf "$GNUPGHOME" nginx.tar.gz.asc
mkdir -p /usr/src
mkdir -p /var/cache/nginx/client_temp
chown -R nginx.nginx /var/cache/nginx
tar -zxC /usr/src -f nginx.tar.gz
rm -rf nginx.tar.gz
cd /usr/src/nginx-$NGINX_VERSION
./configure $CONFIG
make -j$(getconf _NPROCESSORS_ONLN)
make install
rm -rf /etc/nginx/html/
mkdir /etc/nginx/conf.d/
mkdir -p /usr/share/nginx/html/
install -m644 html/index.html /usr/share/nginx/html/
install -m644 html/50x.html /usr/share/nginx/html/
install -m755 objs/nginx /usr/sbin/nginx
install -m755 objs/ngx_http_xslt_filter_module.so /usr/lib/nginx/modules/ngx_http_xslt_filter_module.so
install -m755 objs/ngx_http_image_filter_module.so /usr/lib/nginx/modules/ngx_http_image_filter_module.so
install -m755 objs/ngx_http_geoip_module.so /usr/lib/nginx/modules/ngx_http_geoip_module.so
install -m755 objs/ngx_stream_geoip_module.so /usr/lib/nginx/modules/ngx_stream_geoip_module.so
ln -s ../../usr/lib/nginx/modules /etc/nginx/modules
strip /usr/sbin/nginx*
strip /usr/lib/nginx/modules/*.so
rm -rf /usr/src/nginx-$NGINX_VERSION

	# Bring in gettext so we can get `envsubst`, then throw
	# the rest away. To do this, we need to install `gettext`
	# then move `envsubst` out of the way so `gettext` can
	# be deleted completely, then move `envsubst` back.
	yum install -y gettext
	# Bring in tzdata so users could set the timezones through the environment
	# variables
	yum install -y tzdata
    date -R
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
    date -R
	# forward request and error logs to docker log collector
	ln -sf /dev/stdout /var/log/nginx/access.log
	ln -sf /dev/stderr /var/log/nginx/error.log
