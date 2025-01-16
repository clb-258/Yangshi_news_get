"""央视时政爬取工具，CLB 出品，2025 年 1 月制作。CLB 版权所有。"""

import json
import requests


def request_data(num: int):
    """向央视服务器请求数据"""
    # 向接口请求数据（可以在浏览器里搜到网页之后，用开发者工具来分析对应的接口，需要一定编程基础）
    response = requests.get(f'https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_{num}.jsonp')
    response.encoding = 'utf-8'  # 央视的数据编码似乎没有设置好，需要手动重设
    if response.status_code != 200:  # 假如状态码不是正常的，这个时候在浏览器里调用接口应该会显示错误界面
        # 直接返回就可以
        print(f'第 {num} 页的数据请求失败，服务器报 {response.status_code} 错误')
        return {}
    else:
        # 对数据进行处理
        result_json = response.text[6:-1]  # 去掉它作为js脚本的函数前后缀，得到纯净的json数据
        print(f'第 {num} 页的数据请求成功')
        return json.loads(result_json)  # 把json文本转换成py对象之后返回


def save_data(datas: dict, page: int):
    """整理数据并写入到文件"""
    model_text = ('标题: {0}\n'
                  '发布日期: {1}\n'
                  '主要内容: {2}\n'
                  '详情链接: {3}\n'
                  '头图链接: {4}\n'
                  '关键字: {5}\n\n')  # 设置好写入文本的模板
    with open(f'results/抓取结果_{page}.txt', 'wt') as file:  # 打开对应文件
        count = 1  # 初始化计数器为1，待会就要使用
        for i in datas['data']['list']:  # 找到时政列表，遍历
            text = model_text.format(i.get('title'), i.get('focus_date'), i.get('brief'), i.get('url'), i.get('image'),
                                     i.get('keywords'))  # 用格式化文本的方式，填入信息
            file.write(text)  # 写入文件
            count += 1  # 计数器递加
        file.close()  # 写完后关闭文件
        print(f'第 {page} 页的 {count} 条结果整理成功，结果保存在 抓取结果_{page}.txt 中\n')


def main():
    page_count = int(input('请输入要抓取的页数：'))  # 获得输入，转换成整数
    if page_count < 1:  # 判断并防止非法情况
        print('页数至少为 1')
    else:
        print('开始爬取...\n')
        for i in range(1, page_count + 1):  # 从 1~page_count 的范围遍历页数
            json_dict = request_data(i)  # 请求数据
            if not json_dict:  # 上面返回空字典时，大概率是没有数据可抓了。不管怎么样先退出再说
                print('爬取接口返回了空数据。一定是没有东西能爬了吧...那就退出！')
                return
            else:
                # 数据正常时写入文件
                save_data(json_dict, i)
        print('数据全部爬取完成！请在 result 文件夹里查看。')


if __name__ == "__main__":
    print('央视时政爬取工具，CLB 出品，2025 年 1 月.')
    main()  # 调用主函数
    print('程序退出...')
