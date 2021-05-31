docker rm -f binary_py3
docker run -it --name binary_py3 \
  -v $PWD/binary_dir:/opt/apps/binary_dir \
  -v $PWD/3_binary_py.sh:/opt/apps/3_binary_py.sh \
  ubuntu_18_04_binary_py:0.1