#!/usr/bin/env python
# -*- coding: utf-8 -*-
import API_BaiDu
import db_connect

ak = 'L1imtZ0YPWMXNfMNyj6Gk3aArX4eKQDP'
sk = 'y8xmIhRK4IP2nb1GTOoaqIXoKNAolOfn'

'''
cfg187 = db_connect.get_db_config('C:\\python\\baidumap\\bin\\db_config,xml','ORACLE187')
conn187 = db_connect.get_connect(cfg187)
cursor187=conn187.cursor()

get_pos_sql = 'select station_id,pos_x,pos_y from mk_spc_station where old_id_eqp = 0'
cursor187.execute(get_pos_sql)
result = cursor187.fetchall()
for eachline in result:
    print (eachline)
    in_id = eachline[0]
    in_x = eachline[1]
    in_y = eachline[2]
    new_x_y=API_BaiDu.chg_coordinate(in_x,in_y,5,6,ak,sk)
    print(new_x_y)
    out_x = new_x_y['x']
    out_y = new_x_y['y']
    update_sql = 'update mk_spc_station set pos_x=%s,pos_y=%s,old_id_eqp=%d where station_id = %s' %(out_x,out_y,1,in_id)
    cursor187.execute(update_sql)
    conn187.commit()

'''
new_x_y = API_BaiDu.chg_coordinate(114.32894, 30.585748, 5, 6, ak, sk)
print(new_x_y)
