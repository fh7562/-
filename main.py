import json
from datetime import datetime, timezone, timedelta
from collections import defaultdict
import tkinter as tk
from tkinter import filedialog
import webbrowser
import locale

locale.setlocale(locale.LC_CTYPE,"chinese")

type_mapping = {
    "team": "组队派对",
    "daily_challenge": "每日挑战",
    "challenge": "题库5轮",
    "solo_match": "世界solo",
    "中国solo": "中国solo",
    "battle_royale": "淘汰赛",
    "team_match": "组队匹配",
    "country_streak": "世界国家连胜",
    "province_streak": "中国省份连胜",
    "map_country_streak": "题库国家连胜",
    "solo": "solo派对",
    "main_game": "积分赛",
}


def convert_utc_to_beijing(utc_timestamp):
    utc_time = datetime.utcfromtimestamp(utc_timestamp / 1000).replace(
        tzinfo=timezone.utc
    )
    beijing_time = utc_time.astimezone(timezone(timedelta(hours=8)))
    return beijing_time


def generate_html(json_data):
    data_list = json_data["data"]

    with open("图寻年度总结.html", "w", encoding="utf-8") as html_file:
        html_file.write(
            """<!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="utf-8">
        <style>
body {
    font-family: 'Arial', sans-serif;
    margin: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    position: relative;
    background-image: url("https://i.chao-fan.com/front/farfar-peK8iXqGMzQ-unsplash.jpg?x-oss-process=image/quality,q_50");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.2);
    z-index: 1;
}

#container {
    text-align: center;
    line-height: 1.5;
    padding: 20px;
    z-index: 100;
    position: relative;
}

p {
    margin: 10px 0;
    text-align: center;
    color: rgba(247, 247, 247);
    font-size: 1.8em;
    line-height: 1.5;
}

ul {
    padding-left: 20px;
    text-align: left;
    text-align: center;
    color: rgba(247, 247, 247);
    line-height: 1.5;
    font-size: 1.2em;
    list-style-type: none;
}

br {
    line-height: 2;
}

li {
    list-style-type: disc;
    z-index: 100;
    text-align: center;
    color: rgba(247, 247, 247);
    line-height: 1.5;
    font-size: 1.2em;
    list-style-type: none;
}

a {
    color: rgba(255, 148, 39);
}

a:visited {
    color: rgba(255, 148, 39);
}


.button-container {
    position: fixed;
    bottom: 10%;
    left: 0;
    width: 100%;
    padding: 10px;
    text-align: center;
}

.page-button {
    display: inline;
    color: rgba(255, 148, 39);
    font-size: 1.2em;
    text-decoration: underline;
    background: none;
    border: none;
}

.page {
    display: none;
    z-index: 100;
}

.active {
    display: block;
    z-index: 100;
}

        </style>
        <title>图寻年度总结</title>
    </head>
    <body><div class="overlay"></div>\n"""
        )
        html_file.write("</body>")

        html_file.write('<div id="page1" class="page active">')
        html_file.write(
            f"<p><a href='https://tuxun.fun/user/{data_list[1]['userId']}/'target='_blank'>图寻玩家{data_list[1]['userId']}</a>,你好!</p>\n"
        )
        html_file.write("<p>请查收你的图寻年度总结。</p>\n")
        html_file.write('<div class="button-container">')
        html_file.write('<button class="page-button" onclick="nextPage()">下一页</button>')
        html_file.write("</div>")
        html_file.write("</div>")
        html_file.write('<div id="page2" class="page">')
        daily_data_counts = {}
        daily_data_types = {}

        data_before_2023 = [
            entry for entry in data_list if entry["gmtCreate"] < 1672502400000
        ]
        total_matches_before_2023 = len(data_before_2023)

        if total_matches_before_2023 > 0:
            html_file.write(
                f"<p>你在2023以前就入坑了,堪称图寻老玩家</p><p>截至2023年前,对战总数量为: {total_matches_before_2023} 次</p>\n"
            )

            earliest_match_before_2023 = min(
                data_before_2023, key=lambda entry: entry["gmtCreate"]
            )
            earliest_match_time_before_2023 = convert_utc_to_beijing(
                earliest_match_before_2023["gmtCreate"]
            )
            earliest_match_id_before_2023 = earliest_match_before_2023["gameId"]
            earliest_match_type_before_2023 = earliest_match_before_2023["type"]
            html_file.write(
                f"<p>你最早的{type_mapping.get(earliest_match_type_before_2023, earliest_match_type_before_2023)}对战是在 {earliest_match_time_before_2023.strftime('%Y-%m-%d %H:%M:%S')}</p>\n"
            )

            if earliest_match_id_before_2023 is None:
                earliest_match_with_gameid_before_2023 = next(
                    (
                        entry
                        for entry in data_before_2023
                        if entry["gameId"] is not None
                    ),
                    None,
                )
                if earliest_match_with_gameid_before_2023:
                    earliest_match_with_gameid_time = convert_utc_to_beijing(
                        earliest_match_with_gameid_before_2023["gmtCreate"]
                    )
                    earliest_match_with_gameid_id = (
                        earliest_match_with_gameid_before_2023["gameId"]
                    )
                    earliest_match_with_gameid_type = (
                        earliest_match_with_gameid_before_2023["type"]
                    )
                    html_file.write(
                        f"<p>最早的可复盘的{type_mapping.get(earliest_match_with_gameid_type, earliest_match_with_gameid_type)}对战是在 {earliest_match_with_gameid_time.strftime('%Y-%m-%d %H:%M:%S')},<a href='https://tuxun.fun/solo_game?gameId={earliest_match_with_gameid_id}'target='_blank'>>复盘链接</a></p>\n"
                    )
            else:
                html_file.write(
                    f"<p><a href='https://tuxun.fun/solo_game?gameId={earliest_match_id_before_2023}'target='_blank'>复盘链接</a></p>\n"
                )

        filtered_data = [
            entry
            for entry in data_list
            if 1672502400000 <= entry["gmtCreate"] <= 1704038400000
        ]

        if filtered_data:
            total_matches_2023 = len(filtered_data)
            html_file.write(f"<p>2023年,你游玩图寻的总场数为:</p><p>{total_matches_2023} 场</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")
            html_file.write('<div id="page3" class="page">')

            type_counts = {}
            for entry in filtered_data:
                entry_type = entry["type"]
                if entry_type == "solo_match":
                    if entry["rating"] is None:
                        entry_type = "中国solo"
                        entry["type"] = "中国solo"
                    else:
                        entry_type = "世界solo"

                chinese_type = type_mapping.get(entry_type, entry_type)
                if chinese_type in type_counts:
                    type_counts[chinese_type] += 1
                else:
                    type_counts[chinese_type] = 1

            html_file.write("<p>每个模式游玩次数:</p>\n")
            html_file.write("<ul>\n")
            for entry_type, count in sorted(
                type_counts.items(), key=lambda x: x[1], reverse=True
            ):
                html_file.write(f"<li>{entry_type}: {count} 次</li>\n")
            html_file.write("</ul>\n")
            html_file.write("<p>你最钟爱哪个模式?</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page4" class="page">')
            china_matches = type_counts.get("中国solo", 0)
            world_matches = type_counts.get("世界solo", 0)

            ratio = china_matches / world_matches if world_matches != 0 else 0

            html_file.write("<p>今年,图寻上线了中国匹配beta版</p>\n")
            html_file.write(f"<p>你的中国匹配场数与世界匹配场数比值为: {ratio:.2f}</p>\n")
            if ratio > 1.2:
                html_file.write("<p>你一定是中国匹配爱好者</p>\n")
            elif ratio < 1 / 1.2:
                html_file.write("<p>你一定是世界匹配爱好者</p>\n")
            else:
                html_file.write("<p>你在中国匹配和世界匹配上都表现相近!</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page5" class="page">')
            world_solo_entries = [
                entry
                for entry in filtered_data
                if entry["type"] == "solo_match" and entry["rating"] is not None
            ]
            world_fixed_solo_count = sum(
                1 for entry in world_solo_entries if entry["moveType"] != "noMove"
            )
            world_move_solo_count = len(world_solo_entries) - world_fixed_solo_count
            html_file.write(
                f"<p>在世界solo中</p><p>固定solo次数: {world_fixed_solo_count} 次</p>\n"
            )
            html_file.write(f"<p>移动solo次数: {world_move_solo_count} 次</p>\n")
            ratio = (
                world_move_solo_count / world_fixed_solo_count
                if world_fixed_solo_count != 0
                else 0
            )
            if ratio > 1.2:
                html_file.write("<p>看来你更喜欢移动模式/p>\n")
            elif ratio < 1 / 1.2:
                html_file.write("<p>看来你更喜欢固定模式</p>\n")
            else:
                html_file.write("<p>你对两者雨露均沾</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page6" class="page">')
            non_none_ratings = [
                entry["rating"]
                for entry in filtered_data
                if entry["rating"] is not None
            ]
            if non_none_ratings:
                max_rating = max(non_none_ratings)
                max_rating_entry = next(
                    entry
                    for entry in filtered_data
                    if entry.get("rating") == max_rating
                )
                html_file.write(f"<p>对战了这么多局</p><p>你的最高分是 {max_rating} 分, 太强了!</p>\n")
                html_file.write(
                    f"<p>在{convert_utc_to_beijing(max_rating_entry['gmtCreate']).strftime('%m月%d日 %H:%M:%S')},</p><p>一场<a href='https://tuxun.fun/solo_game?gameId={max_rating_entry.get('gameId', 'N/A')}'target='_blank'>{type_mapping.get(max_rating_entry['type'], max_rating_entry['type'])}</a>使你达到了最高分</p>\n"
                )
            else:
                html_file.write("<p>你没有参加积分比赛,再接再厉吧。</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page7" class="page">')
            for entry in filtered_data:
                beijing_time = convert_utc_to_beijing(entry["gmtCreate"])
                date = beijing_time.date()

                if date in daily_data_counts:
                    daily_data_counts[date] += 1
                else:
                    daily_data_counts[date] = 1

                entry_type = entry["type"]

                if date in daily_data_types:
                    daily_data_types[date].append(entry_type)
                else:
                    daily_data_types[date] = [entry_type]

            gmt_create_times = [
                convert_utc_to_beijing(entry["gmtCreate"]) for entry in filtered_data
            ]
            earliest_match_2023 = min(
                filtered_data, key=lambda entry: entry["gmtCreate"]
            )
            earliest_match_time = convert_utc_to_beijing(
                earliest_match_2023["gmtCreate"]
            )
            earliest_match_id = earliest_match_2023["gameId"]
            earliest_match_type = earliest_match_2023["type"]
            if earliest_match_id is None:
                html_file.write(
                    f"<p>在{earliest_match_time.strftime('%m月%d日 %H:%M:%S')}</p><p>你进行了一场{type_mapping.get(earliest_match_type, earliest_match_type)}</p><p>这是你最早的图寻对战</p>\n"
                )
                non_empty_gameid_entries = [
                    entry for entry in filtered_data if entry["gameId"] is not None
                ]
                earliest_entry = min(
                    non_empty_gameid_entries, key=lambda entry: entry["gmtCreate"]
                )

                earliest_gameid_time = convert_utc_to_beijing(
                    earliest_entry["gmtCreate"]
                )
                earliest_gameid_id = earliest_entry["gameId"]
                earliest_gameid_type = earliest_entry["type"]
                html_file.write(
                    f"<p>最早的可复盘的对战是一场<a href='https://tuxun.fun/solo_game?gameId={earliest_gameid_id}'target='_blank'>{type_mapping.get(earliest_gameid_type, earliest_gameid_type)}</a></p><p>发生在{earliest_gameid_time.strftime('%m月%d日 %H:%M:%S')}</p>\n"
                )
            else:
                html_file.write(
                    f"<p>在2023年的{earliest_match_time.strftime('%m月%d日 %H:%M:%S')}</p><p>你进行了一场<a href='https://tuxun.fun/solo_game?gameId={earliest_match_id}'target='_blank'>{type_mapping.get(earliest_match_type, earliest_match_type)}</a></p><p>这是你最早的图寻对战。</p>\n"
                )
            html_file.write("<p>你的水平进步了多少?</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page8" class="page">')
            morning_range = range(6, 12)
            afternoon_range = range(12, 18)
            evening_range = range(18, 24)
            midnight_range = range(0, 6)

            time_counts = defaultdict(int)
            for time in gmt_create_times:
                hour = time.hour

                if hour in midnight_range:
                    time_counts["凌晨"] += 1
                elif hour in morning_range:
                    time_counts["上午"] += 1
                elif hour in afternoon_range:
                    time_counts["下午"] += 1
                elif hour in evening_range:
                    time_counts["晚上"] += 1
            most_played_period = max(time_counts, key=time_counts.get)

            html_file.write(f"<p>你最喜欢在{most_played_period}玩图寻</p>\n")
            html_file.write("<p>各个时段的数量:</p>\n")
            html_file.write("<ul>\n")
            for period in ["凌晨", "上午", "下午", "晚上"]:
                count = time_counts.get(period, 0)
                html_file.write(f"<li>{period}: {count} 次</li>\n")
            html_file.write("</ul>\n")

            before_6am_times = [time for time in gmt_create_times if time.hour < 6]
            if before_6am_times:
                closest_time = min(
                    before_6am_times,
                    key=lambda time: abs((time.hour * 60 + time.minute) - (6 * 60)),
                )

                closest_entry = next(
                    entry
                    for entry in filtered_data
                    if convert_utc_to_beijing(entry["gmtCreate"]) == closest_time
                )
                closest_game_type = closest_entry["type"]
                closest_game_id = closest_entry["gameId"]

                if closest_game_id:
                    html_file.write(
                        f"<p>在{closest_time.strftime('%m月%d日 %H:%M:%S')}</p><p>你还在玩<a href='https://tuxun.fun/solo_game?gameId={closest_game_id}'target='_blank'>{type_mapping.get(closest_game_type, closest_game_type)}</a></p>\n"
                    )
                else:
                    html_file.write(
                        f"<p>在{closest_time.strftime('%m月%d日 %H:%M:%S')}</p><p>你还在玩{type_mapping.get(closest_game_type, closest_game_type)}。</p>\n"
                    )
            else:
                html_file.write("<p>你没有熬夜玩图寻,早睡大神!</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page9" class="page">')

            num_of_days = len(daily_data_counts)
            html_file.write(f"<p>今年,你有 {num_of_days} 天都在游玩图寻</p>\n")
            if num_of_days == 365:
                html_file.write("<p>为全勤大神点赞。</p>\n")
            elif num_of_days >= 180:
                html_file.write("<p>活跃度过半,很不错!</p>\n")
            daily_challenge_dates = set(
                date
                for date, entry_types in daily_data_types.items()
                if "daily_challenge" in entry_types
            )
            num_of_daily_challenge_days = len(daily_challenge_dates)
            html_file.write(
                f"<p>你打卡了 {num_of_daily_challenge_days} 天的每日挑战</p><p>你有几天抽到了会员?</p>\n"
            )
            if num_of_daily_challenge_days == 365:
                html_file.write("<p>你是日挑全勤玩家,太厉害了!</p>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page10" class="page">')
            max_date, max_count = max(daily_data_counts.items(), key=lambda x: x[1])
            count = max(daily_data_counts.items(), key=lambda x: x[1])
            html_file.write(
                f"<p>{max_date.strftime('%m月%d日')}是一个特殊的日子</p><p>你一共对战了 {max_count} 场</p>\n"
            )
            max_date_types = daily_data_types[max_date]
            max_date_type_counts = {
                entry_type: max_date_types.count(entry_type)
                for entry_type in set(max_date_types)
            }
            max_date_most_common_type, max_date_most_common_count = max(
                max_date_type_counts.items(), key=lambda x: x[1]
            )
            html_file.write(
                f"<p>其中,你玩了 {max_date_most_common_count} 场{type_mapping.get(max_date_most_common_type, max_date_most_common_type)}</p><p>太令人上头了</p>\n"
            )
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page11" class="page">')

            monthly_data_counts = {}
            for date, count in daily_data_counts.items():
                month = date.month
                if month in monthly_data_counts:
                    monthly_data_counts[month] += count
                else:
                    monthly_data_counts[month] = count

            max_month, max_month_count = max(
                monthly_data_counts.items(), key=lambda x: x[1]
            )
            html_file.write(
                f"<p>你的对战记录最多的月份是{max_month}月</p><p>共对战了 {max_month_count} 把</p>\n"
            )

            max_month_types = [
                entry_type
                for date, entry_types in daily_data_types.items()
                if date.month == max_month
                for entry_type in entry_types
            ]
            max_month_type_counts = {
                entry_type: max_month_types.count(entry_type)
                for entry_type in set(max_month_types)
            }
            max_month_most_common_type, max_month_most_common_count = max(
                max_month_type_counts.items(), key=lambda x: x[1]
            )
            html_file.write(
                f"<p>其中,你在这个月玩了 {max_month_most_common_count} 场{type_mapping.get(max_month_most_common_type, max_month_most_common_type)}</p><p>这个月一定有很多时间吧!</p>\n"
            )
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")
            html_file.write('<div id="page12" class="page">')
            rating_change_counts = defaultdict(list)
            none_count = 0
            for entry in filtered_data:
                rating_change = entry.get("ratingChange")
                if rating_change is not None:
                    rating_change_counts[rating_change].append(entry)
                else:
                    none_count += 1
            max_rating_change = max(rating_change_counts.keys())
            max_rating_change_entries = rating_change_counts[max_rating_change]
            html_file.write(f"<p>你上分最多的对战上了 {max_rating_change} 分!</p>\n")
            html_file.write("<ul>\n")
            for entry in max_rating_change_entries:
                game_id = (
                    "<a href='https://tuxun.fun/solo_game?gameId="
                    + entry["gameId"]
                    + "'target='_blank'>世界solo</a>"
                    if "gameId" in entry and entry["gameId"]
                    else "积分赛"
                )
                game_time = convert_utc_to_beijing(entry["gmtCreate"]).strftime(
                    "%m月%d日 %H:%M:%S"
                )
                html_file.write(f"<li>{game_id},时间: {game_time}</li>\n")
            html_file.write("</ul>\n")
            min_rating_change = min(rating_change_counts.keys())
            min_rating_change_entries = rating_change_counts[min_rating_change]
            html_file.write(f"<p>但是,你掉分最多的场次掉了 {-min_rating_change} 分。</p>\n")
            html_file.write("<ul>\n")
            for entry in min_rating_change_entries:
                game_id = (
                    "<a href='https://tuxun.fun/solo_game?gameId="
                    + entry["gameId"]
                    + "'target='_blank'>世界solo</a>"
                    if "gameId" in entry and entry["gameId"]
                    else "积分赛"
                )
                game_time = convert_utc_to_beijing(entry["gmtCreate"]).strftime(
                    "%m月%d日 %H:%M:%S"
                )
                html_file.write(f"<li>{game_id},时间: {game_time}</li>\n")
            html_file.write("</ul>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")
            html_file.write('<div id="page13" class="page">')
            party_entries = [
                entry for entry in filtered_data if entry.get("partyId") is not None
            ]
            total_party_count = len(set(entry["partyId"] for entry in party_entries))
            html_file.write(
                f"<p>你一共参加了 {total_party_count} 场派对</p><p>如果图寻只能有一个模式</p><p>那么一定是派对</p>\n"
            )
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")
            html_file.write('<div id="page14" class="page">')

            season_entries = [
                entry["season"]
                for entry in filtered_data
                if entry["season"] is not None
            ]
            season_counts = {}
            for season in set(season_entries):
                season_counts[season] = season_entries.count(season)

            html_file.write("<p>图寻从2023年7月1日起重新实施赛季制</p>\n")
            html_file.write("<ul>\n")
            for season, count in season_counts.items():
                if season == "230701":
                    html_file.write("<li>7月-9月赛季: " + str(count) + " 次对战</li>\n")
                elif season == "231001":
                    html_file.write("<li>10月-12月赛季: " + str(count) + " 次对战</li>\n")
                else:
                    html_file.write(f"<li>{season}: {count} 次</li>\n")
            html_file.write("</ul>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page15" class="page">')
            time_diff_entries = [
                {
                    "type": entry["type"],
                    "gameId": entry.get("gameId"),
                    "time_diff": max(0, entry["gmtEnd"] - entry["gmtCreate"]),
                }
                for entry in filtered_data
            ]

            def convert_to_hms(milliseconds):
                seconds, milliseconds = divmod(milliseconds, 1000)
                minutes, seconds = divmod(seconds, 60)
                return f"{int(minutes)}分钟{int(seconds)}秒"

            valid_time_diff_entries = [
                entry for entry in time_diff_entries if entry["time_diff"] > 0
            ]
            solo_match_entries = [
                entry
                for entry in valid_time_diff_entries
                if (
                    entry["type"] == "中国solo"
                    or entry["type"] == "solo_match"
                    or entry["type"] == "solo"
                )
                and entry["time_diff"] > 5000
            ]
            sorted_solo_match_entries = sorted(
                solo_match_entries, key=lambda entry: entry["time_diff"]
            )
            html_file.write("<p>最快的solo对战:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[:3]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")

            html_file.write("<p>最慢的solo对战:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[-3:]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")

            html_file.write('<div id="page16" class="page">')
            solo_match_entries = [
                entry
                for entry in valid_time_diff_entries
                if (entry["type"] == "team" or entry["type"] == "team_match")
                and 5400000 > entry["time_diff"] > 5000
            ]
            sorted_solo_match_entries = sorted(
                solo_match_entries, key=lambda entry: entry["time_diff"]
            )

            html_file.write("<p>最快的团队对战:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[:3]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")

            html_file.write("<p>最慢的团队对战:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[-3:]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")
            html_file.write('<div class="button-container">')
            html_file.write(
                '<button class="page-button" onclick="prevPage()">上一页</button>'
            )
            html_file.write(
                '<button class="page-button" onclick="nextPage()">下一页</button>'
            )
            html_file.write("</div>")
            html_file.write("</div>")
            html_file.write('<div id="page17" class="page">')

            solo_match_entries = [
                entry
                for entry in valid_time_diff_entries
                if entry["type"] == "challenge" and entry["time_diff"] > 5000
            ]

            sorted_solo_match_entries = sorted(
                solo_match_entries, key=lambda entry: entry["time_diff"]
            )

            html_file.write("<p>最快的题库5题:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[:3]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")

            html_file.write("<p>最慢的题库5题:</p>\n")
            html_file.write("<ul>\n")
            for entry in sorted_solo_match_entries[-3:]:
                time_diff_hms = convert_to_hms(entry["time_diff"])
                html_file.write(
                    f"<li>时长为{time_diff_hms},对战类型为<a href='https://tuxun.fun/solo_game?gameId={entry['gameId']}'target='_blank'>{type_mapping.get(entry['type'], entry['type'])}</a></li>\n"
                )
            html_file.write("</ul>\n")

        else:
            html_file.write("<p>在2023年没有找到相关对战。再接再厉吧!</p>\n")
        html_file.write(
            """
        <div class="button-container">
            <button class="page-button" onclick="prevPage()">上一页</button>
            <button class="page-button" onclick="nextPage()">下一页</button>
        </div>
        </div>
        <div id="page18" class="page">
            <p>感谢所有图寻玩家的贡献和付出。</p>
            <p>2024年已经到来</p>
            <p>让我们在新的一年继续</p>
            <p><a href='https://tuxun.fun'target='_blank'>探索世界，找到你。</a></p>
            <div class="button-container">
                <button class="page-button" onclick="prevPage()">上一页</button>
            </div>
        </div>
        """
        )

        html_file.write(
            """
        <script>
            let currentPage = 1;

            function showPage(pageNumber) {
                document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
                document.getElementById(`page${pageNumber}`).classList.add('active');
                currentPage = pageNumber;
            }

            function nextPage() {
                showPage(currentPage + 1);
            }

            function prevPage() {
                showPage(currentPage - 1);
            }
        </script>
        """
        )
        html_file.write("</body>\n")
        html_file.write("</html>\n")


def on_click(json_string):
    try:
        json_data = json.loads(json_string)
    except json.JSONDecodeError as e:
        tk.messagebox.showerror(title="错误", message=f"JSON格式不正确: {e}")
        return
    generate_html(json_data)
    tk.messagebox.showinfo(title="成功", message="已保存至程序所在目录下的“图寻年度总结.html”")
    webbrowser.open("图寻年度总结.html")
    window.destroy()




def open_url():
    webbrowser.open("https://tuxun.fun/api/v0/tuxun/history/listSelf?count=1000000")


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding='utf-8') as file:
            file_content = file.read()
            on_click(file_content)


window = tk.Tk()
window.title("图寻年度总结生成器")
window.geometry("700x300")

window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)

label = tk.Label(
    window,
    text="""请先点击访问网页(使用登录图寻的浏览器),之后将网页所有的内容复制并保存为txt文件，最后点击"打开文件"并选择。\n                 
by专业航线规划员""",
)
label.grid(row=0, column=0, columnspan=3, sticky="nsew")

url_button = tk.Button(window, text="访问网页", command=open_url)
url_button.grid(row=1, column=0, sticky="e", padx=5)

open_file_button = tk.Button(window, text="打开文件", command=open_file)
open_file_button.grid(row=1, column=1, sticky='w', padx=5)


window.mainloop()
