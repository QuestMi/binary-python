## binary-python 使用说明

**使用前，请确保电脑上已经安装docker**


### 一、基础环境镜像准备（基于ubuntu18.04、python3.6进行二进制）

**注：不同平台（ubuntu、windows、os）进行二进制的代码，不能跨平台使用，即ubuntu上二进制的代码，只能ubuntu上运行，其他平台使用会报错。**

**1、基于ubuntu18.04构建二进制环境镜像;**

    /bin/bash 1_build_image.sh

### 二、二进制 文件夹/文件 准备、运行

**1、将需要 二进制的文件夹或文件 拷贝到 binary_dir目录下，参考如下；**

    binary_dir 
    ├── app			# 需要二进制的文件夹 
         ├── server.py  
         └── test_binary.py

**2、根据需求调整不需要加密的文件（即 -I 参数，-i、-o、-m无需调整）；**

    # 打开 3_binary_py.sh 
    """
    source /opt/apps/python/bin/activate  # 激活虚拟环境
    jmpy -i /opt/apps/binary_dir -I server.py,location_.*\.py -m 0 # 执行二进制
    
    python代码 加密
    参数说明：
        -i | --input_file_path    待加密文件或文件夹路径，可是相对路径或绝对路径
        -o | --output_file_path   加密后的文件输出路径，默认在input_file_path下创建dist文件夹，存放加密后的文件
        -I | --ignore_files       不需要加密的文件或文件夹，逗号分隔
        -m | --except_main_file   不加密包含__main__的文件(主文件加密后无法启动), 值为0、1。 默认为1
    
    """

**3、运行容器 ；**

    /bin/bash 2_run_image.sh  # 运行后会自动进入容器 

**4、运行二进制脚本** 

    /bin/bash 3_binary_py.sh 
    
    # 运行结果如下
    """
    binary_dir 
    ├── app		                 # 需要二进制的文件夹 
    │    ├── server.py  
    │    └── test_binary.py
    └── dist
        └── binary_dir			 # 二进制后的文件夹
            └── app
                ├── server.py
                └── test_binary.so  
    """

