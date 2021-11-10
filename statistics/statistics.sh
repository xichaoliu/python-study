#!/bin/bash
:<<EOF
统计代码行数
使用方法1：单行命令模式 -a 提交人 -f 统计提交记录id -t 统计结束提交记录id
eg：./statistics.sh -a liuxichao -f b15e4bcaf6e5dea090f9d12ab3ef29d91c5022bb -t cb96184fa838b61df369751878717901195a9e7f
EOF
#统计文件类型
count_files="html,css,js,json,vue,py,java,ftl,sh,md"	
# 生成提交作者正则
grAuthorPattern() {
	authorPattern=''
	for aut in $*
	do
		if [ -z $authorPattern ]
		then
			authorPattern=$aut;
		else
			authorPattern="${authorPattern}\|${aut}"
		fi
	done
	echo $authorPattern
}
endCommitId="HEAD"
if [ $1 ]
then
	# 获取参数
	while getopts "a:f:t:" arg
	do
		case $arg in
			a)
			author=$OPTARG
			;;
			f)
			startCommitId=$OPTARG
			;;
			t)
			endCommitId=$OPTARG
			;;
			*)
			exit
		esac
	done
else
	read -p "Please Input author: " iauthor
	author=$iauthor
	echo "作者名称: $author"
	read -p "Pleas Input earlier commitid: " istartId
	startCommitId=$istartId
	echo "查询开始提交id: $startCommitId"
	read -p "Pleas Input recent commitid: " iendId
	if [ -n "$iendId" ]
	then
		endCommitId=$iendId
	fi
	echo "查询结束提交id: $endCommitId"
fi
if [[ -z $author || -z $startCommitId || -z $endCommitId ]]
then 
	echo "error: missing args"
	exit
fi
regStr=''
# 分割类型字符串
OLD_IFS="$IFS"
IFS=","
arr=($count_files)
IFS="$OLD_IFS"
# 生成更是正则字符串
for type in ${arr[@]}
do
	len=${#regStr}
	if [ $len -gt 1 ]
	then
		regStr="${regStr}|.${type}"
	else
		regStr=".${type}"
	fi
done
author=($author)
author=`grAuthorPattern ${author[@]}`
git log $startCommitId..$endCommitId --author=$author --pretty=tformat: --numstat | grep -E $regStr | awk -vt=$count_files 'BEGIN {
	tAdd=0; 
	tSubs=0; 
	tLoc=0;
	split(t, typeArr, ",")
	} 
	{
		for (i in typeArr) {
			subStr = "." typeArr[i];
			ret = match($3, subStr)
			if (ret != 0) {
				key = "*." typeArr[i];
				countStr = subArr[key]
				split(countStr, countArr, ",")
				subAdd = countArr[1] > 0 ? countArr[1] : 0;
				subSubs = countArr[2] > 0 ? countArr[2] : 0;
				subLoc = countArr[3] > 0 ? countArr[3] : 0;
				subAdd += $1;
				subSubs += $2;
				subLoc += $1-$2;
				subArr[key] = subAdd "," subSubs "," subLoc;
 			}
		}
		tAdd +=$1; 
		tSubs += $2; 
		tLoc += $1-$2;
	} END {
		printf "\n"
		for (n in subArr) {
			countStr = subArr[n]
			split(countStr, countArr, ",")
			printf "file：%-15s added lines:%-6s removed lines:%-6s diff lines: %-6s\n", n, countArr[1], countArr[2], countArr[3]
		}
		printf "\n"
		printf "total--> added lines:%s, removed lines:%s, diff lines: %s\n", tAdd, tSubs, tLoc
}'