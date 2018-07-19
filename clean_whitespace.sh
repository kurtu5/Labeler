echo dos2unix all files
 find . -type d -name .git -prune -o -type f  -exec dos2unix {} \;
echo remove all trailing whitespace
 find . -type d -name .git -prune -o -type f  -exec sed -ie 's/[ ]*$//' {} \;
echo find any tabs
 find . -type d -name .git -prune -o -type f -exec grep -l '	' {} \; | grep -v pycache
