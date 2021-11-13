#!/bin/bash
:<<EOF
统计代码行数
EOF
#统计文件类型
count_files="html,css,js,json,vue,py,java,ftl,sh"	
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
# 切换分支
checkoutBranch() {
	currentBranch=`git branch | sed -n 's/\* //p'`
	read -p "Please input branch name: ($currentBranch) " branch
	if [ -n "$branch" ]
	then
		git checkout $branch
		if [ $? != 0 ]
		then 
			checkoutBranch
		else
		currentBranch=$branch
		echo -e "统计分支: $currentBranch\n"
		fi
	else
		echo -e "统计分支: $currentBranch\n"
	fi
}
read -p "Input file types,split with ',': (html,css,js,json,vue,py,java,ftl,sh) " itype
	if [ -n "$itype" ]
	then
		count_files=$itype
	fi
echo -e "统计文件类型：$count_files\n"
checkoutBranch
author=`git config --global user.name`
read -p "Please input authors,split with ',': ($author) " iauthor
	if [ -n "$iauthor" ]
	then
		author=$iauthor
	fi
echo -e "作者名称: $author\n"
since='1970-01-01'
read -p "Pleas input start time: ($since) " isince
	if [ -n "$isince" ]
	then
		since=$isince
	fi
echo -e "统计起始日期: $since\n"
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
OLD_IFS="$IFS"
IFS=","
author=($author)
IFS="$OLD_IFS"
author=`grAuthorPattern ${author[@]}`

echo -en "Please waiting...  \n"

git log --since=$since --author=$author --pretty=tformat: --numstat | grep -E $regStr | awk -vt=$count_files 'BEGIN {
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
			printf "file：%-10s added lines:%-7s removed lines:%-7s diff lines: %-7s\n", n, countArr[1], countArr[2], countArr[3]
		}
		printf "\n"
		printf "total--> added lines:%s, removed lines:%s, diff lines: %s\n", tAdd, tSubs, tLoc
}'