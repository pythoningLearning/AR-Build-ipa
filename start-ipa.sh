#!/bin/bash
path=`dirname $0`
cd "${path}"
echo -e "\nInput a number from below items"
echo "1. build ipa debug"
echo "2. build ipa release"

read aNum
case $aNum in
    1)  python ipa-build.py 'debug'
    ;;
    2)  python ipa-build.py 'release'
    ;;
    *)  echo 'You input error! stop'
    ;;
esac
