import requests
import urllib.parse
import json
from typing import List, Tuple, Optional


class ChongqingMetroBatchQuery:
    def __init__(self):
        self.base_url = "https://www.cqmetro.cn/Front/html/TakeLine!queryYsTakeLine.action"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_travel_time(self, start_station: str, end_station: str) -> Optional[int]:
        """
        获取两站点间的行程时间

        参数： start_station: 起始站点
            end_station: 终点站点

            return:行程时间（秒），失败返回None
        """
        try:
            # URL编码站点名称
            encoded_start = urllib.parse.quote(start_station, encoding='utf-8')
            encoded_end = urllib.parse.quote(end_station, encoding='utf-8')

            # 构建请求参数
            params = {
                'entity.startStaName': encoded_start,
                'entity.endStaName': encoded_end
            }

            # 发送请求
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()

            # 解析JSON响应
            data = response.json()

            if data.get('success') and data.get('result') and len(data['result']) > 0:
                return data['result'][0].get('needTimeScope')
            else:
                return None

        except Exception:
            return None

    def batch_query(self, stations: List[str]) -> List[Tuple[str, str, Optional[int]]]:
        """
        批量查询站点间隔时间

            参数：stations: 站点列表

            return:查询结果列表，每个元素为(起始站, 终点站, 时间秒数)
        """
        if len(stations) % 2 != 0:
            raise ValueError("站点数量必须为偶数")

        results = []

        # 每两个站点为一组进行查询
        for i in range(0, len(stations), 2):
            start_station = stations[i].strip()
            end_station = stations[i + 1].strip()

            travel_time = self.get_travel_time(start_station, end_station)
            results.append((start_station, end_station, travel_time))

        return results

    def print_results(self, results: List[Tuple[str, str, Optional[int]]]):
        """
        打印查询结果
        """
        for start, end, time_seconds in results:
            if time_seconds is not None:
                time_minutes = time_seconds / 60
                print(f"{start} -> {end}: {time_seconds}秒 ({time_minutes:.1f}分钟)")
            else:
                print(f"{start} -> {end}: 查询失败")


def main():

    metro_query = ChongqingMetroBatchQuery()

    print("请输入站点名称，用空格或换行分隔，站点数量必须为偶数")
    print("每两个站点为一组：第1个为起始站，第2个为终点站")
    print("输入完成后按回车键结束输入，再按一次回车开始查询\n")
    print(f"输入：")
    stations = []
    while True:
        line = input().strip()
        if not line:
            break
        # 支持空格分隔的多个站点
        stations.extend(line.split())

    if len(stations) == 0:
        print("未输入任何站点")
        return

    if len(stations) % 2 != 0:
        print(f"错误：输入了{len(stations)}个站点，必须为偶数个")
        return

    print(f"开始查询{len(stations) // 2}组站点...")
    print("-" * 50)

    try:
        # 批量查询
        results = metro_query.batch_query(stations)

        # 打印结果
        metro_query.print_results(results)

    except Exception as e:
        print(f"查询过程中出现错误: {e}")


def batch_query_from_list(station_list: List[str]) -> None:

    metro_query = ChongqingMetroBatchQuery()

    try:
        results = metro_query.batch_query(station_list)
        metro_query.print_results(results)
    except Exception as e:
        print(f"查询错误: {e}")



if __name__ == "__main__":

    main()