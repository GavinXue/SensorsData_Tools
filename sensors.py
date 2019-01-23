# -*- coding: utf-8 -*-
# !/usr/bin/python3
# author: Gavin Xue
# last edit: 20190121

import requests
import json
import os
import sys
from urllib import parse
import pandas as pd
import urllib3

# 禁用安全请求警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SensorsProject(object):
    def __init__(self, url=None, project="default", username=None, password=None):
        self.token = None
        self.error = None

        self.url = self.delete_url_slash(url)
        self.project = project
        self.username = username
        self.password = password
        if not self.error:
            self.obtain_token()
        self.sa_event_design = EventDesign()
        if self.token:
            self.generate_event_table()

    def delete_url_slash(self, sa_url):
        """
        :param url: 用户配置或输入的 url
        :return: 去除最后斜线后的 url
        """
        try:
            parse_url = parse.urlsplit(sa_url)
            if parse_url.scheme:
                return parse_url.scheme + '://' + parse_url.netloc
            else:
                return 'http://' + parse_url.path.split('/')[0]
        except Exception as e:
            self.error = "请输入正确的 URL！"
            return ''

    def obtain_token(self):
        """
        此方法使用配置文件中 sensorsdata 的参数
        此方法用于获取 Login 接口中返回的 Cookie，
        :return: cookie 中的 token
        """
        print("-- begin to login in --")
        api_url = self.url + '/api/auth/login'
        params = {
            'project': self.project
        }
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'User-Agent': 'Paw/3.1 (Macintosh; OS X/10.12.6) GCDHTTPRequest'
        }
        data = {
            'username': self.username,
            'password': self.password
        }
        try:

            response = requests.post(url=api_url, params=params, headers=headers, data=json.dumps(data),
                                     timeout=1, verify=False)

            if 'error' in response.json().keys():
                self.error = response.json()['error']
                return None
            elif response.json()['token']:
                print("-- get the token successfully --")
                self.token = response.json()['token']
                return None
        except Exception as e:
            self.error = '请输入正确的URL：' + str(e)

    def generate_event_table(self):
        print('-- begin to obtain project events info --')
        api_url = self.url + '/api/events/all'
        results = requests.get(url=api_url, params={'project': self.project, 'invisible': True},
                               headers={'sensorsdata-token': self.token}, verify=False).text
        df_event = pd.read_json(results)

        api_url_properties = self.url + '/api/event/properties'
        properties = requests.get(api_url_properties, params={'project': self.project, 'show_all': True,
                                                              'cache': 'false',
                                                              'events': ','.join([name for name in df_event["name"]])},
                                  verify=False, headers={'sensorsdata-token': self.token}).json()
        prop_list = []
        for event_prop in properties.items():
            prop_list += event_prop[1]['event']

        df_prop = pd.DataFrame(prop_list)

        df = df_prop.join(df_event.set_index('id'), on='event_id', lsuffix='_prop', rsuffix='_event')
        df.rename(index=str, columns={'cname_prop': 'property_cn', 'name_prop': 'property_en',
                                      'cname_event': 'event_cn', 'name_event': 'event_en',
                                      'data_type': 'data_type_en', 'id': 'property_id'}, inplace=True)
        data_type_map = {'bool': 'BOOL', 'string': '字符串', 'list': '列表',
                         'number': '数值', 'date': '日期', 'datetime': '时间'}
        df['data_type_cn'] = df['data_type_en'].map(data_type_map)

        self.sa_event_design.event_table = df
        self.sa_event_design.df_event = df[['event_id', 'event_en', 'event_cn', 'virtual', 'visible']].drop_duplicates()
        self.sa_event_design.df_prop = df[['property_en', 'property_cn', 'property_id',
                                           'data_type_en', 'data_type_cn']].drop_duplicates()

        print('-- obtaining project events info completed --')

    # todo: 生成一个对应的获取环境中 设计的属性
    def export_event_design(self, virtual_event=False, default_prop=False, invisible_event=True):
        print('-- begin to export event design --')
        df_export = self.sa_event_design.event_table[['event_en', 'event_cn', 'visible', 'property_en',
                                                      'property_cn', 'data_type_cn', 'db_column_name']]
        # 去除各种筛选条件
        if not default_prop:
            # 如果一个事件没有自定义属性，需要指定一个无自定义属性的字段
            has_prop_event = df_export.loc[~df_export.db_column_name.str.contains('p__')].event_en.unique()
            tmp = df_export.loc[~df_export.event_en.isin(has_prop_event)][['event_en', 'event_cn',
                                                                           'visible', 'property_en',
                                                                           'property_cn',
                                                                           'data_type_cn', 'db_column_name']]
            tmp.property_en, tmp.property_cn, tmp.data_type_cn, tmp.db_column_name = '-', '-', '-', '-',
            tmp.drop_duplicates(['event_en'], inplace=True)
            df_export = df_export.loc[~df_export.property_en.str.contains('\$')]
            df_export = df_export.append(tmp)

        if not virtual_event:
            df_export = df_export.loc[~df_export.event_en.str.contains('\$')]

        if not invisible_event:
            df_export = df_export.loc[df_export.visible]

        # todo 增加对隐藏属性的支持
        # if not invisible_prop:
        #     df_export = df_export.loc[df_export.is_in_use]

        df_export.drop(['db_column_name'], axis=1, inplace=True)
        df_export.rename(index=str, columns={'event_en': '事件英文名', 'event_cn': '事件中文名',
                                             'visible': '事件是否可见', 'property_en': '属性英文名',
                                             'property_cn': '属性中文名', 'data_type_cn': '数据类型'}, inplace=True)

        print('-- totally export property {} lines --'.format(df_export.shape[0]))
        result_path = '/'.join(os.path.realpath(sys.argv[0]).split('/')[:-4]) + '/export_event_design.xlsx'
        df_export.to_excel(result_path, index=False, encoding='utf-8')
        return result_path

    def update_cname(self, upload_event_design, update_event=False, update_prop=False, cover_old_name=False):
        """
        更新 SA 环境中的中文变量名
        :param upload_event_design: 上传的事件设计
        :param update_event: 确认是否需要更新事件的中文名
        :param update_prop: 确认是否需要更新属性的中文名
        :param cover_old_name: 确认是否覆盖原有已经命名的中文名
        :return:
        """
        upload_event_design.check_prop_coherence()
        if upload_event_design.prop_coherence_error:
            raise Exception("事件设计存在一致性问题，请返回工具箱主页，\n进行一次中英文变量一致性检查！")

        result_report = ''
        if update_event:
            df_tmp = upload_event_design.df_event.merge(self.sa_event_design.df_event,
                                                        left_on='event_en', right_on='event_en',
                                                        suffixes=('_update', '_sa'))
            if cover_old_name:
                tmp_json = df_tmp[['event_cn_update', 'event_id']].rename(
                    columns={'event_cn_update': 'cname'}).to_json(orient="records")
                update_event_json = json.loads(tmp_json)
            else:
                tmp_json = df_tmp[df_tmp.event_cn_sa == df_tmp.event_en][['event_cn_update', 'event_id']].rename(
                        columns={'event_cn_update': 'cname'}).to_json(orient="records")
                update_event_json = json.loads(tmp_json)
            print(' {} event name updated...'.format(len(update_event_json)))
            update_result = requests.post(self.url + "/api/events/multimeta", params={'project': self.project},
                                          headers={'sensorsdata-token': self.token,
                                                   'Content-Type': 'application/json; charset=utf-8'},
                                          data=json.dumps(update_event_json))
            if "error" in update_result.text:
                raise Exception(update_result.text)
            else:
                result_report += '共 {} 个事件显示名更新成功...\n'.format(len(update_event_json))

        if update_prop:
            df_tmp = upload_event_design.df_prop.merge(self.sa_event_design.df_prop,
                                                       left_on='property_en', right_on='property_en',
                                                       suffixes=('_update', '_sa'))
            if cover_old_name:
                tmp_json = df_tmp[['property_cn_update', 'property_id']].rename(
                    columns={'property_cn_update': 'cname'}).to_json(orient="records")
                update_prop_json = json.loads(tmp_json)
            else:
                tmp_json = df_tmp[df_tmp.property_en == df_tmp.property_cn_sa][['property_cn_update', 'property_id']]\
                    .rename(columns={'property_cn_update': 'cname'}).to_json(orient="records")
                update_prop_json = json.loads(tmp_json)
            update_result = requests.post(self.url + "/api/property/meta", params={'project': self.project},
                                          headers={'sensorsdata-token': self.token,
                                                   'Content-Type': 'application/json; charset=utf-8'},
                                          data=json.dumps({'property': update_prop_json}))
            if "error" in update_result.text:
                raise Exception(update_result.text)
            else:
                result_report += '共 {} 个属性显示名更新成功...\n'.format(len(update_prop_json))

        return result_report


class EventDesign:
    def __init__(self):
        self.event_table = pd.DataFrame()
        self.df_event = pd.DataFrame()
        self.df_prop = pd.DataFrame()
        self.user_table = pd.DataFrame()
        self.event_qty = None
        self.prop_qty = None
        self.filename = None
        self.prop_coherence_error = None

    def upload_event_design(self, filename):
        self.filename = filename
        df = pd.read_excel(filename, None, header=None)  # header must be None
        if df.get("事件表", pd.DataFrame()).empty:
            raise Exception("error: 事件设计中没有命名'事件表'的 Sheet！")
        else:
            # Parse the event design sheet
            self.event_table = self.parse_event_table(df.get("事件表"))

            self.df_event = self.event_table[['event_en', 'event_cn']].drop_duplicates()
            self.df_prop = self.event_table[['property_en', 'property_cn',
                                             'data_type_cn', 'data_type_en']].drop_duplicates()
            self.event_qty = self.event_table['event_en'].unique().size
            self.prop_qty = self.event_table['property_en'].unique().size
            self.user_table = df.get("用户表", pd.DataFrame())
            self.prop_coherence_error = None

    @staticmethod
    def parse_event_table(df):
        rows, cols = df.shape
        index_col = []
        for index, item in df.iterrows():
            if index == 0:
                item[1] = '公共属性'
                item[2] = '公共属性'
            elif not pd.isnull(item[1]):
                pass
            else:
                item[1] = df.iloc[index - 1, 1]
                item[2] = df.iloc[index - 1, 2]
                item[7] = df.iloc[index - 1, 7]

        for col in range(cols):
            # 需要保证Column的排序是按模板来排的
            if sum(df[col].isin(['事件编号', '事件英文变量名',
                                 '事件显示名', '属性英文变量名', '事件属性显示名', '属性值类型'])) > 0:
                index_col.append(col)

        if not index_col == [0, 1, 2, 3, 4, 5]:
            raise Exception("error: 请确定事件设计表是否按照标准模板中 ['事件编号', '事件英文变量名', '事件显示名', "
                            "'属性英文变量名', '事件属性显示名', '属性值类型'] 顺序排列！")
        else:
            df_tmp = df[[1, 2, 3, 4, 5, 6, 7]].dropna(how='all')
            df_tmp.columns = ['event_en', 'event_cn', 'property_en', 'property_cn',
                              'data_type_cn', 'example', 'track_type']

            data_type_map = {'BOOL': 'bool', '字符串': 'string', '列表': 'list',
                             '数值': 'number', '日期': 'date', '时间': 'datetime'}
            df_tmp['data_type_en'] = df_tmp['data_type_cn'].map(data_type_map)
            # 处理事件只有一个预置属性的问题
            df2 = df_tmp.groupby(by='event_en').size().loc[lambda x: x == 1]
            df_one = df_tmp[df_tmp['event_en'].isin(df2.index.values) &
                            ~df_tmp['event_en'].isin(['公共属性'])].fillna('-')
            df_result = pd.concat([df_tmp, df_one])

            df_result = df_result.dropna(subset=['property_en'])
            df_result = df_result[df_result.property_en != '属性英文变量名']
            return df_result

    def check_prop_coherence(self):
        """验证事件设计中属性的 变量名、中文名、属性类型是否一致
        :return:
        """
        errors = self.check_var_error(self.df_prop, 'property_en', 'property_cn') + \
                 self.check_var_error(self.df_prop, 'property_en', 'data_type_cn') + \
                 self.check_var_error(self.df_prop, 'property_cn', 'property_en') + \
                 self.check_var_error(self.df_prop, 'property_cn', 'data_type_cn')
        self.prop_coherence_error = errors

    @staticmethod
    def check_var_error(df, group_var, check_var):
        df1 = df.groupby([group_var])[check_var].unique()
        errors = []
        for value in df1.index.values:
            if len(df1[value]) > 1:
                error = '%s：%s 有多个对应%s，%s' % (group_var, value, check_var, str(df1[value]))
                error = error.replace('property_en', '英文变量名') \
                    .replace('property_cn', '属性显示名').replace('data_type_cn', '属性值类型')
                errors.append(error)
        return errors


if __name__ == '__main__':
    # sa = SensorsProject()
    filepath = "xxx"
    e_d = EventDesign()
    e_d.upload_event_design(filepath)
    e_d.verify_prop_format()
