# spark-docker_proj
云计算与大数据平台课-github仓库

项目功能：基于分布式Spark引擎的书籍推荐、基于mongodb的推荐结果存储，并可根据命令行传参得到用户id，以此根据用户id进行推荐。

文件介绍：
data_process文件夹：存放项目源数据文件，和进行过情感分析之后的结果文件（在本地运行），最终需要使用的只有u_proc.data、u.item文件，将其移动至spark-docker_proj/spark-docker/data/ml-100k/路径下即可使用。
spark_docker文件夹：存放项目文件，主要由docker-compose.yml文件进行部署，实现一主两从的spark分布式集群，和一个mongodb数据库存储结构。使用docker-compose.yml环境之前需要修改一下路径以连接到两个镜像。

部署：
本项目使用到了2个image文件
分别为：zsf_mongo_image.tar 对应mongo数据库的镜像
        zsf_spark_image.tar 对应spark分布式引擎的镜像
        
配置好环境路径后，使用spark_docker文件夹的docker-compose.yml进行docker-compose up命令即可部署。

如果从头部署，在使用mongodb之前需要初始化用户和密码（新建用户信息）。
示例代码如下：


