#!/usr/bin/env python
# -*- coding: utf-8 -*-
#百度地图常用接口

import urllib
import hashlib
import json

#返回状态值翻译
def get_status(status):
    status_code = {'0':'正常',  \
                   '1':'服务器内部错误', \
                   '10':'上传内容超过8M', \
                   '101':'AK参数不存在', \
                   '102':'MCODE参数不存在，mobile类型mcode参数必需', \
                   '200':'APP不存在，AK有误请检查再重试',  \
                   '201':'APP被用户自己禁用，请在控制台解禁', \
                   '202':'APP被管理员删除', \
                   '203':'APP类型错误', \
                   '210':'APP IP校验失败', \
                   '211':'APP SN校验失败', \
                   '220':'APP Referer校验失败', \
                   '230':'APP Mcode码校验失败', \
                   '240':'APP 服务被禁用', \
                   '250':'用户不存在', \
                   '251':'用户被自己删除', \
                   '252':'用户被管理员删除', \
                   '260':'服务不存在', \
                   '261':'服务被禁用', \
                   '301':'永久配额超限，限制访问', \
                   '302':'天配额超限，限制访问', \
                   '401':'当前并发量已经超过约定并发配额，限制访问', \
                   '402':'当前并发量已经超过约定并发配额，并且服务总并发量也已经超过设定的总并发配额，限制访问', \
                   '4': '转换失败', \
                   '21': 'from非法', \
                   '22': 'to非法', \
                   '24': 'coords格式非法', \
                   '25': 'coords个数非法，超过限制', \
                   '26': '参数错误'
                   }
    return status_code(status)

#通过url，ak，sk编码产生sn方法
def get_sn(query_url,ak,sk):
    query_url = query_url + '&ak=%s' %(ak)
    encodedStr = urllib.parse.quote(query_url, safe="/:=&?#+!$,;'@()*[]")   #编码中文字符url
    rawStr = encodedStr + '%s' %(sk)
    raw_pls = urllib.parse.quote_plus(rawStr)
    hash = hashlib.md5()
    hash.update(raw_pls.encode('utf-8'))
    ak_plus = '&ak=' + ak + '&sn='+ hash.hexdigest()
    return ak_plus

#按照要求转换坐标系（)
# source_type:
# 1：GPS设备获取的角度坐标，wgs84坐标;
# 2：GPS获取的米制坐标、sogou地图所用坐标;
# 3：google地图、soso地图、aliyun地图、mapabc地图和amap地图所用坐标，国测局（gcj02）坐标;
# 4：3中列表地图坐标对应的米制坐标;
# 5：百度地图采用的经纬度坐标;
# 6：百度地图采用的米制坐标;
# 7：mapbar地图坐标;
# 8：51地图坐标
#target_type :5：bd09ll(百度经纬度坐标)
#6：bd09mc(百度米制经纬度坐标);
def chg_coordinate(pos_x,pos_y,source_type,target_type,ak,sk):
    url_head = 'http://api.map.baidu.com'
    query_url = '/geoconv/v1/?coords=%s,%s&from=%s&to=%s' %(pos_x,pos_y,source_type,target_type)
    encodeurl = urllib.parse.quote(query_url, safe="/:=&?#+!$,;'@()*[]")
    access_code = get_sn(encodeurl,ak,sk)
    request_url = url_head + query_url + access_code
    print(request_url)
    request = urllib.request.urlopen(request_url)
    res = request.read().decode()
    res_json = json.loads(res)
    status = res_json['status']
    if status == 0:
        result = res_json['result'][0]
        return result
    else:
        result = get_status(status)
        return result

#根据地址转换经纬度
#address : 1、标准的结构化地址信息，如北京市海淀区上地十街十号 【推荐，地址结构越完整，解析精度越高】
#2、支持“*路与*路交叉口”描述方式，如北一环路和阜阳路的交叉路口
#city:地址所在的城市名。用于指定上述地址所在的城市，当多个城市都有上述地址时，该参数起到过滤作用，但不限制坐标召回城市。
def get_address_x_y(address,city,ak,sk):
    url_head = 'http://api.map.baidu.com'
    if city == '':
        query_url = '/geocoder/v2/?address=%s&output=json' % (address)
    else:
        query_url = '/geocoder/v2/?address=%s&city=%s&output=json' % (address, city)
    access_code = get_sn(query_url, ak, sk)
    request_url = url_head + query_url + access_code
    encodeurl = urllib.parse.quote(request_url, safe="/:=&?#+!$,;'@()*[]")
    request = urllib.request.urlopen(encodeurl)
    res = request.read().decode()
    res_json = json.loads(res)
    status = res_json['status']
    if status == 0:
        temp = res_json['result']['location']
        result = {'x':temp['lng'],'y':temp['lat']}
        return result
    else:
        result = get_status(status)
        return result
