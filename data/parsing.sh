cp $1 temp
tr [A-Z] [a-z] < temp > temp1
mv temp1 temp

sed -i "s/aren't/are not/g" temp
sed -i "s/can't/can not/g" temp
sed -i "s/couldn't/could not/g" temp
sed -i "s/don't/do not/g" temp
sed -i "s/didn't/did not/g" temp
sed -i "s/doesn't/does not/g" temp
sed -i "s/don't/do not/g" temp
sed -i "s/hadn't/had not/g" temp
sed -i "s/hasn't/has not/g" temp
sed -i "s/haven't/have not/g" temp
sed -i "s/isn't/is not/g" temp
sed -i "s/wasn't/was not/g" temp
sed -i "s/won't/would not/g" temp
sed -i "s/wouldn't/would not/g" temp

mv temp parsed_$1
