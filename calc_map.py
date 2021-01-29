import os
import sys
import json
import glob
import numpy as np
import xml.etree.ElementTree as ET
from voc_eval import voc_eval


def json_load(json_file):
    with open(json_file, "r") as f:
        data = json.load(f)
    return data


def calc_map(class_names, annopath, json_res):
    datas = json_load(json_res)
    npos_list, recall_list, wujian_list, ap_list = [], [], [], []
    recall_num_list, wujian_num_list = [], []
    res = []
    for class_name in class_names:
        data = datas[class_name]
        npos, recall_num, wujian_num, recall, wujian, ap = voc_eval(data, annopath, class_name, ovthresh=0.5, use_07_metric=False)
        print('{}: recall {:.3f}, wujian {:.3f}, ap {:.3f}'.format(class_name, recall, wujian, ap))
        item = '{},{:.0f},{:.0f},{:.0f},{:.3f},{:.3f},{:.3f}\n'.format(class_name, npos, recall_num, wujian_num, recall, wujian, ap)
        #print('{}: ap {}'.format(class_name, ap))
        ap_list.append(ap)
        npos_list.append(npos)
        recall_list.append(recall)
        wujian_list.append(wujian)
        recall_num_list.append(recall_num)
        wujian_num_list.append(wujian_num)

        res.append(item)
    map_value = sum(ap_list)/len(ap_list)
    mean_call_rate = sum(recall_list)/len(recall_list)
    mean_wujian_rate = sum(wujian_list)/len(wujian_list)
    print('map:{:.3f}'.format(map_value))
    with open('res.txt', 'w') as f:
        line_head = "类别名称,类别数,检出数,误检数,检出率,误检率,AP\n"
        f.write(line_head)
        f.write(''.join(res))
        line = 'sum,{:.0f},{:.0f},{:.0f},{:.3f},{:.3f},{:.3f}\n'.format(sum(npos_list), sum(recall_num_list), sum(wujian_num_list), sum(recall_num_list)/(sum(npos_list)+1e-6), sum(wujian_num_list)/(sum(npos_list)+1e-6), map_value)
        print(line)
        f.write(line)


def get_names(annopath, json_res):
    classes_name = []
    xmls = glob.glob(annopath + "*.xml")
    for xml in xmls:
        tree = ET.parse(xml)
        for obj in tree.findall('object'):
            name = obj.find("name").text
            if name not in classes_name:
                classes_name.append(name)

    datas = json_load(json_res)
    data_names = datas.keys()
    return [i for i in classes_name if i in data_names]


if __name__ == "__main__":
    annopath = 'data/Annotations/'
    json_res = "res.json"

    classes = get_names(annopath, json_res)  # Extracts class labels from xmls
    print(classes)
    print(len(classes))
    calc_map(classes, annopath, json_res)

