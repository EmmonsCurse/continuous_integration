#!/usr/bin/env bash

set -eo pipefail

ROOT=`dirname "$0"`
ROOT=`cd "$ROOT/.."; pwd`
export OUTPUT=$ROOT/output
export OUTPUT_BIN=$ROOT/build
export DATA_ROOT=$ROOT/data
export TOOLS_ROOT=$ROOT/tools
export CASE_ROOT=$ROOT/bin

mkdir -p $DATA_ROOT
cd $DATA_ROOT

if [ ! -f c++/resnet50/model/__model__ ]; then
    echo "==== Download data and models ===="
    wget --no-proxy https://sys-p0.bj.bcebos.com/inference/c++-infer.tgz --no-check-certificate
    tar -zxf c++-infer.tgz
fi

cd -
bash $CASE_ROOT/resnet.sh
