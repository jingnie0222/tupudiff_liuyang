#!/bin/bash

version=("online" "test")
#version=("online")
host=("cache01.tupu.djt.ted" "10.134.30.37")
#host=("10.134.30.37")
port=("5555" "5555")
query_file='poem_test.txt'
test_version='poem_test'
mode=2       #0:仅对比pvtype、vrid  1:对比pvtype、vrid、标题、答案  2:对比pvtype、vrid、标题、答案、摘要

desc_file='desc'
add_file='add'
diff_file='diff'

today=`date +%Y%m%d_%H%M%S`

for ((i=0;i<${#version[@]};i++));
do
python3 tupush_diff.py --queryfile=${query_file} --resultfile=${version[i]}.result --req_config="forceQuery=1" \
                      --host="${host[i]}" --port="${port[i]}" --mode=${mode}  --version="${version[i]}"
done
mkdir ${diff_file}${today}
python3 result_statistic.py --online_result=online.result --test_result=test.result --query_file=${query_file} \
                            --desc_file=${desc_file}${today}.html --add_file=${add_file}${today}.html --diff_file=${diff_file}${today}.html --test_version=${test_version} --today=${today}
mkdir ${today}
mv online.result online.result${today}
mv test.result test.result${today}
mv online.result${today} test.result${today} ${desc_file}${today}.html ${add_file}${today}.html diff_new${today}.html ${diff_file}${today} ${diff_file}${today}.html ${today}/
rsync -avzr ${today} root@10.143.45.197:/search/odin/nginx/html
