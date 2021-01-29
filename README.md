## 该工具用来评价目标检测模型的性能，主要计算mAP，检出率，漏检率；
## 需要准备的文件
   (1) 在dada/Annotations/ 文件夹里面存放标注数据，标注格式跟Pacal VOC相同
  （2）res.json, 检测的结果。
## res.json格式说明
   {
       "class_name1":[
                        [img_name, score, x1, y1, x2, x2]
                        [img_name, score, x1, y1, x2, x2]
                        [img_name, score, x1, y1, x2, x2]
                        ...
                    ],
       "class_name2":[类别2],
       "class_name3":[类别3],
       ...
   }
## 运行python3 calc_map.py 测试结果保存在res.txt中。
