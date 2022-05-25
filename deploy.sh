#!/bin/bash
if [ "$1" = "" ]
then
    echo "第1引数に関数名を指定して下さい。"
    # 処理を中断。
    exit 1
fi
if [ "$2" = "" ]
then
    echo "第2引数にソースのパスを指定して下さい。"
    # 処理を中断。
    exit 1
fi
FUNCTION_NAME=$1
SOURCE_PATH=$2
echo "$FUNCTION_NAMEを更新します。"
ZIPFILE="$FUNCTION_NAME.zip"
S3BUCKET="ai-call-temporary"
S3KEY="work/$ZIPFILE"
source ~/.bash_profile
ZIPFILE=$ZIPFILE \
  SOURCE_PATH=$SOURCE_PATH \
  docker-compose up &&
  ZIPFILE=$ZIPFILE \
  SOURCE_PATH=$SOURCE_PATH \
  docker-compose down -v && \
(aws s3 cp $SOURCE_PATH/$ZIPFILE s3://$S3BUCKET/$S3KEY && \
  wincmd aws lambda \
    update-function-code \
    --function-name $FUNCTION_NAME \
    --s3-bucket $S3BUCKET \
    --s3-key $S3KEY \
    --publish) ; \
aws s3 rm s3://$S3BUCKET/$S3KEY ; \
rm $SOURCE_PATH/$ZIPFILE
