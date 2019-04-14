# -*- coding: utf-8 -*-
#!/usr/bin/env bash
pushd `dirname $0` > /dev/null
BASE_DIR=`pwd -P`
popd > /dev/null

#############
# Functions
#############
function logging {
    echo "[INFO] $*"
}
function build_venv {
    if [ ! -d env ]; then
        virtualenv env
    fi
    . env/bin/activate
    pip install -r requirements.txt

}
function creator_db {
    logging "makemigrations"
	python "${BASE_DIR}/mysite/manage.py" "makemigrations"

    logging "makemigrations" "account"
    python "${BASE_DIR}/mysite/manage.py" "makemigrations" "account"   

    logging "migrate"
	python "${BASE_DIR}/mysite/manage.py" "migrate"

}
function write_data_db {
    logging "initdb_user.py"
    python3 "${BASE_DIR}/mysite/initdb_user.py"
    logging "initdb_account.py"
    python3 "${BASE_DIR}/mysite/initdb_account.py"
}


function launch_webapp {
    python3 "${BASE_DIR}/mysite/manage.py" "runserver" "8000"
}
#############
# Main
#############
cd ${BASE_DIR}
OPT_ENV_FORCE=$1

build_venv

#创建数据库表，适合添加数据库后操作，能重复操作，不会破坏数据。
if [ "${OPT_ENV_FORCE}x" == "-cx" ];then    
    creator_db
fi
# 创建数据表、创建超级用户，破坏数据?!!!(2018.01.21)。
if [ "${OPT_ENV_FORCE}x" == "-cax" ];then    
    creator_db
    python "${BASE_DIR}/mysite/manage.py" "createsuperuser" #创建超级用户
fi

# 初始化数据库。创建数据表,删除数据后再加载数据。谨慎操作！！！
if [ "${OPT_ENV_FORCE}x" == "-ix" ];then    
    logging "Clean"
    rm -rf "${BASE_DIR}/mysite/db.sqlite3"

    rm -rf "${BASE_DIR}/mysite/account/migrations/0*"
    ls "${BASE_DIR}/mysite/account/migrations/"
    
    creator_db
    write_data_db
fi


launch_webapp
