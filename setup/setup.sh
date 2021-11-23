#!bin/bash
ENV_NAME=random-graph-generator
ENV_PATH=setup/environment.yml

source ~/anaconda3/etc/profile.d/conda.sh
conda env create -n $ENV_NAME -f $ENV_PATH
conda activate $ENV_NAME
ipython kernel install --user --name=$ENV_NAME-kernel
conda deactivate
jupyter notebook random_graph_generator.ipynb