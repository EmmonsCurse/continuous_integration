
#!/bin/sh

ROOT_PATH=$1

if [ -e data ]
then
   mv data data.bak
fi
if [ ! -e data.tgz ]
then
    wget https://sys-p0.bj.bcebos.com/models/PaddleNLP/similarity_net/data.tgz --no-check-certificate
fi
tar -zxf data.tgz


#prepare data
if [ -e args_test_data ]
then
    echo "args_test_data has already existed"
else
    #ln -s /ssd3/models_test/models_args/PaddleNLP/similarity_net/data args_test_data
    #ln -s ${ROOT_PATH}/data/PaddleNLP/similarity_net/data args_test_data
    ln -s data args_test_data
fi

#prepare pre_model
if [ -e args_test_model_files ]
then
    echo "args_test_model_files has already existed"
else
    #ln -s /ssd3/models_test/models_args/PaddleNLP/similarity_net/model_files args_test_model_files
    #ln -s ${ROOT_PATH}/data/PaddleNLP/similarity_net/model_files args_test_model_files
    ln -s data args_test_model_files
fi

#
if [ -e  args_test_output_1 ]
then
    /bin/rm -rf args_test_output_1
    mkdir args_test_output_1
fi
if [ -e  args_test_output_2 ]
then
    /bin/rm -rf args_test_output_2
    mkdir args_test_output_2
fi
