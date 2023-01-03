import threading
import time
from typing import List, Dict

from requests import Response, Session, post

from datetime import timedelta

from erepublik import Citizen, utils

CONFIG = {
    'email': 'jiqimaono2@163.com',
    'password': 'yuiop[',
    'interactive': True,
    'fight': True,
    'debug': False,
    'battle_launcher': {
        121672: {"auto_attack": False, "regions": [661]},
        125530: {"auto_attack": False, "regions": [259]},
        125226: {"auto_attack": True, "regions": [549]},
        124559: {"auto_attack": True, "regions": [176]}
    },
    'telegram_chat_id': '901406392',
    'telegram_token': '1062108968:AAGRkXhOpA9qTuQ0Se8YFY0JnrKwImH_F4k'
}


def telextt(msg):
    xtttoken = '1255503748:AAGKqHbDh_SkZoFgTHE_761li730EMu8OYo'
    xttid = 988474037
    api_url = "https://api.telegram.org/bot{}/sendMessage".format(xtttoken)
    # print(api_url)
    post(api_url,
         json=dict(chat_id=xttid, text=msg, parse_mode="Markdown"))


def telextt2(msg):
    xtttoken = '1255503748:AAGKqHbDh_SkZoFgTHE_761li730EMu8OYo'
    xttid = 1496901954
    api_url = "https://api.telegram.org/bot{}/sendMessage".format(xtttoken)
    print(api_url)
    post(api_url,
         json=dict(chat_id=xttid, text=msg, parse_mode="Markdown"))


def work_train_buy_eat(player: Citizen):
    try:
        player.update_citizen_info()
        player.update_inventory()
        player.work()
        player.train()
        player.collect_weekly_reward()
        # player.buy_monetary_market_offer()
        player.update_job_info()
        ot_time = player.my_companies.next_ot_time
        delta = utils.now() - ot_time
        print("work_train_buy next overtime", delta)
        if not player.is_levelup_reachable:
            print(player.eat())
        if delta > timedelta(minutes=50):
            player.work_ot()
            offers = player.get_monetary_offers()
            offer_id = offers[0]['offer_id']
            print("work_train_buy ", player._post_economy_exchange_purchase(10, 62, offer_id))
            player.update_citizen_info()
            # if (player.energy.available > 1400) and int(utils.now().hour) > 17:
            # print("work_train_buy ",player.work_as_manager())
    except Exception as inst:
        print("work_train_buy exception", inst)
        player.report_error("Task error: work_train_buy")


def no_terrain_fight(player: Citizen, id, count=1):
    battle_to_fight = player.all_battles.get(id)
    if battle_to_fight.invader.country.id == player.details.citizenship:
        battle_side = battle_to_fight.invader
    if battle_to_fight.defender.country.id == player.details.citizenship:
        battle_side = battle_to_fight.defender
    if player.all_battles.get(id).is_rw:
        print(battle_to_fight, " is rw! count 3")
        count = 3
    for div in battle_to_fight.div.values():
        # print(div.id)
        # print(div.div)
        # print(div.terrain)
        if div.div < 4 and div.terrain == 0:
            player._post_military_change_weapon(id, int(div.id), 7)
            player.fight(battle_to_fight, div, side=battle_side, count=count)


def after_summer_fight(player: Citizen, id, count=1, findempty = True):
    battle_to_fight = player.all_battles.get(id)
    if battle_to_fight.invader.country.id == player.details.citizenship:
        battle_side = battle_to_fight.invader
    if battle_to_fight.defender.country.id == player.details.citizenship:
        battle_side = battle_to_fight.defender
    if player.all_battles.get(id).is_rw:
        print(battle_to_fight, " is rw! count 3")
        count = 3

    for div in battle_to_fight.div.values():
        # print(div.id)  10046316
        # print(div.div)  3
        # print(div.terrain)  0
        if div.div < 4 and div.terrain == 0:
            player._post_military_change_weapon(id, int(div.id), 7)
            # player.fight(battle_to_fight, div, side=battle_side, count=1)

            place = get_hit_status(player, id, div=div.div)
            time.sleep(2)
            if not findempty:
                if not place == 1:
                    continue
            else:
                if not place == 0:
                    continue
            player.fight(battle_to_fight, div, side=battle_side, count=count)

    for div in range(1, 4):
        # print(div.id)
        # print(div.div)
        # print(div.terrain)
        place = get_hit_status(player, id, div=div)
        time.sleep(2)
        if not findempty:
            if not place == 1:
                continue
        else:
            if not place == 0:
                continue
        player.fight(battle_to_fight, div, side=battle_side, count=count)
        # if div.div < 4 and div.terrain == 0:
        #     player._post_military_change_weapon(id,int(div.id),7)
        #     player.fight(battle_to_fight, div, side=battle_side, count=count)

def after_summer_fight_div(player: Citizen, id, divint, count=1, findempty = True):
    # just fight in divint
    battle_to_fight = player.all_battles.get(id)
    if battle_to_fight.invader.country.id == player.details.citizenship:
        battle_side = battle_to_fight.invader
    if battle_to_fight.defender.country.id == player.details.citizenship:
        battle_side = battle_to_fight.defender
    if player.all_battles.get(id).is_rw:
        print(battle_to_fight, " is rw! count 3")
        count = 3

    for div in battle_to_fight.div.values():
        # print(div.id)  10046316
        # print(div.div)  3
        # print(div.terrain)  0
        if div.div == divint and div.terrain == 0:
            player._post_military_change_weapon(id, int(div.id), 7)
            # player.fight(battle_to_fight, div, side=battle_side, count=1)

            # place = get_hit_status(player, id, div=div.div)
            # time.sleep(2)
            # if not findempty:
            #     if not place == 1:
            #         continue
            # else:
            #     if not place == 0:
            #         continue
            player.fight(battle_to_fight, div, side=battle_side, count=count)

    for div in range(1, 4):
        # print(div.id)
        # print(div.div)
        # print(div.terrain)
        place = get_hit_status(player, id, div=div)
        time.sleep(2)
        if not findempty:
            if not place == 1:
                continue
        else:
            if not place == 0:
                continue
        player.fight(battle_to_fight, div, side=battle_side, count=count)
        # if div.div < 4 and div.terrain == 0:
        #     player._post_military_change_weapon(id,int(div.id),7)
        #     player.fight(battle_to_fight, div, side=battle_side, count=count)


def inform_new_and_checkBH(player, battles, new_battle_list, bh_watch_list, guaji: bool = True, fight_rw: bool = False):
    # after summer use after_summer_fight
    # summer use no_terrain_fight
    for id in battles:
        print(player.all_battles[id])
        delta = utils.now() - player.all_battles[id].start
        time.sleep(2)
        if (delta < timedelta(minutes=15) and
            delta > timedelta(minutes=0)):
            newbattleinfo = str(id) + ":" + str(player.all_battles[id].zone_id)
            if not newbattleinfo in new_battle_list:
                print("inform_new_and_checkBH found new battle! ", newbattleinfo)
                if player.energy.available > 400:
                    if not player.all_battles[id].is_rw:
                        # no_terrain_fight(player, id)
                        after_summer_fight(player, id)
                    if fight_rw:
                        if player.all_battles[id].is_rw:
                            after_summer_fight(player, id)
                # message = 'find battle: ' + str(player.all_battles[id])
                message2 = '/hit 123 https://www.erepublik.com/en/military/battlefield/' + str(id) + ' cn '
                message3 = " new battle:  " + str(delta)
                message4 = 'https://www.erepublik.com/en/military/battlefield/' + str(id)

                if guaji:
                    if (not player.all_battles[id].is_rw):
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                else:
                    post(player.telegram.api_url,
                         json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                # post(player.telegram.api_url,
                #      json=dict(chat_id=player.telegram.chat_id, text=message3, parse_mode="Markdown"))
                # post(player.telegram.api_url,
                #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                ####################################################################################
                telextt(message2)
                #####################################################################################
                new_battle_list.append(newbattleinfo)
                # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                continue
        if (delta > timedelta(minutes=71)):
            for i in range(1, 4):
                bh_watch = str(id) + ":" + str(player.all_battles[id].zone_id) + ":" + str(i)
                if bh_watch in bh_watch_list:
                    continue
                place = get_my_status(player, id, div=i)
                if place > 1:
                    print(bh_watch)
                    if not bh_watch in bh_watch_list:
                        message = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                                  + "  check BH in Div: " + str(i)
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message, parse_mode="Markdown"))
                        ####################################################################
                        telextt(message)
                        ######################################################################
                        print(message)
                    bh_watch_list.append(bh_watch)
                else:
                    print("check BH done: ", "div ", i, place)
            time.sleep(2)
    return new_battle_list, bh_watch_list


def guaji_fangti(player: Citizen, hrs, battles, battles2):
    player.update_citizen_info()
    player.update_inventory()
    print(player.energy)
    print("hrs: ", hrs)
    # print("missing energy: ", player.energy.limit * 2 - player.energy.available)
    # print("consider-full energy: ", player.energy.limit * 2 - hrs * 10 * player.energy.interval)
    print("consider-full time: ",
          (player.energy.limit * 2 - player.energy.available) / (10 * player.energy.interval))
    # energy.limit: 1060  energy.recoverable: 769 energy.recovered: 1060 energy.available: 1829 energy.interval: 30
    print(player.food)
    if not player.is_levelup_reachable:
        print(player.eat())
    if ((player.energy.limit * 2 - player.energy.available < int(hrs * 10 * player.energy.interval)) and
        (player.energy.available > 500)):
        # hit, div, dam = find_avaiable_hits(player, battles, battles2, findempty=True)
        hit, div, dam = find_avaiable_hits_di_d1_3(player, battles, battles2, findempty=True)
        print("guaji_fangti hit, div, dam: {} {} {} ".format(hit, div, dam))
        if hit > 0:
            print("lets hit")
            # player.fight(hit, div, player.details.citizenship, count=1)
            after_summer_fight_div(player,hit,div)
            # player.fight_until_damage(hit, player.details.citizenship, count=1,
            #                           division=div, damage_final=dam)
        else:
            hit, div, dam = find_avaiable_hits(player, battles, battles2, findempty=True)
            print("guaji_fangti hit, div, dam: {} {} {} ".format(hit, div, dam))
            if hit > 0:
                print("lets hit")
                # player.fight(hit, div, player.details.citizenship, count=1)
                after_summer_fight_div(player, hit, div)
                # player.fight_until_damage(hit, player.details.citizenship, count=1,
                #                           division=div, damage_final=dam)
            print("no avaiable battle! ")
        if not player.is_levelup_reachable:
            print(player.eat())
    if not player.details.current_region == player.details.residence_region:
        player.travel_to_region(player.details.residence_region)

def _battle_monitor(player: Citizen, hrs: float):
    """Launch battles. Check every 5th minute (0,5,10...45,50,55) if any battle could be started on specified regions
    and after launching wait for 90 minutes before starting next attack so that all battles aren't launched at the same
    time. If player is allowed to fight, do 100 hits on the first round in players division.

    :param player: Logged in Citizen instance
    ":type player: Citizen
    """
    global CONFIG
    finished_war_ids = {*[]}
    war_data = CONFIG.get('start_battles', {})
    war_ids = {int(war_id) for war_id in war_data.keys()}
    next_attack_time = player.now
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=59)
    print("_battle_monitor 309", next_attack_time)
    new_battle_list = []
    bh_watch_list = []
    while not player.stop_threads.is_set():
        try:
            player.update_war_info()
            battles_list = cus_sorted_battles(player)
            battles = battles_list[0] + battles_list[2]
            battles2 = battles_list[4]
            # guaji_fangti(player, hrs, battles, battles2 )
            utils.now()
            new_battle_list, bh_watch_list = inform_new_and_checkBH(player, battles, new_battle_list, bh_watch_list)
            player.update_citizen_info()
            if not player.details.current_region == player.details.residence_region:
                print("player.details.current_region", player.details.current_region)
                print("player.details.residence_region", player.details.residence_region)
                # player.travel_to_region(player.details.residence_region)
                player.travel_to_residence()
                data = {
                    "toCountryId": 14,
                    "inRegionId": 395,
                }
                player._post_main_travel("moveAction", **data)
                # player.travel_to_holding(player.my_companies.holdings[0])
            print("_battle_monitor 288", battles)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except:
            player.report_error("Task error: start_battles")
        ###########################################################
        work_train_buy_eat(player)
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=350))
        print("149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))

def _battle_monitor_after_summer_inherit_from_summer(player: Citizen, hrs: float):
    """Launch battles. Check every 5th minute (0,5,10...45,50,55) if any battle could be started on specified regions
    and after launching wait for 90 minutes before starting next attack so that all battles aren't launched at the same
    time. If player is allowed to fight, do 100 hits on the first round in players division.

    :param player: Logged in Citizen instance
    ":type player: Citizen
    """
    global CONFIG
    finished_war_ids = {*[]}
    war_data = CONFIG.get('start_battles', {})
    war_ids = {int(war_id) for war_id in war_data.keys()}
    next_attack_time = player.now
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=59)
    print("_battle_monitor 309", next_attack_time)
    new_battle_list = []
    bh_watch_list = []
    while not player.stop_threads.is_set():
        try:
            player.update_war_info()
            battles_list = cus_sorted_battles(player)
            battles = battles_list[0] + battles_list[2]
            battles2 = battles_list[4]
            # guaji_fangti(player, hrs, battles, battles2 )
            utils.now()
            new_battle_list, bh_watch_list = inform_new_and_checkBH(player, battles, new_battle_list, bh_watch_list)
            player.update_citizen_info()
            if not player.details.current_region == player.details.residence_region:
                print("player.details.current_region", player.details.current_region)
                print("player.details.residence_region", player.details.residence_region)
                # player.travel_to_region(player.details.residence_region)
                player.travel_to_residence()
                data = {
                    "toCountryId": 14,
                    "inRegionId": 395,
                }
                player._post_main_travel("moveAction", **data)
                # player.travel_to_holding(player.my_companies.holdings[0])
            print("_battle_monitor 288", battles)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except:
            player.report_error("Task error: start_battles")
        ###########################################################
        work_train_buy_eat(player)
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=350))
        print("149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))


def get_hit_status(player, battle_id: int, div: int = 4,
                   target_hit=[7636970, 7087490, 6246857, 6880339, 2858573, 4511581, 5905067]) -> int:
    # return {}
    battle = player.all_battles.get(battle_id)
    round_id = battle.zone_id
    division = div if round_id % 4 > 0 else 11
    division = div
    resp = player._post_military_battle_console(battle_id, 'battleStatistics', round_id=round_id,
                                                division=division).json()
    resp.pop('rounds', None)
    print("get_hit_status resp ", resp)

    # {'14': {'fighterData': {'1': {'citizenId': 1542079, 'citizenName': 'jiqimaono2', 'country_name': 'China',
    #                               'citizenAvatar': 'https://cdnt.erepublik.net/7s5Qg3dx1IiFOtYYGRa3yJK8URM=/30x30/smart/avatars/Citizens/2009/06/11/820af46e7726ab11dd955c73954a22e0.jpg',
    #                               'country_permalink': 'China', 'for_country_id': 14, 'value': '14,358,582',
    #                               'raw_value': 14358582, 'reward': False},
    #                         '2': {'citizenId': 5368708, 'citizenName': 'Legen017', 'country_name': 'Spain',
    #                               'citizenAvatar': 'https://cdnt.erepublik.net/OAGxWEnN2unJA6xViZIX5UKVg-Q=/30x30/smart/avatars/Citizens/2011/11/23/a0c1f09662432ea6a9ec0a5d6f0d2015.jpg?a76e9aa274a07715d40d260ae3042f62',
    #                               'country_permalink': 'Spain', 'for_country_id': 14, 'value': '847,617',
    #                               'raw_value': 847617, 'reward': False}}, 'pages': 0}, '45': {'fighterData': {
    #     '1': {'citizenId': 4080491, 'citizenName': 'MisterTerminator', 'country_name': 'Japan',
    #           'citizenAvatar': 'https://cdnt.erepublik.net/RVjn9scT7VjWJXmL4ZiiZGlIGvA=/30x30/smart/avatars/Citizens/2010/11/14/38296b897dbf99d9a4c4279bdc865cd9.jpg?c858079a0ff17f1a0bf7d0bf9e7facee',
    #           'country_permalink': 'Japan', 'for_country_id': 45, 'value': '18,760,980', 'raw_value': 18760980,
    #           'reward': False}, '2': {'citizenId': 4580613, 'citizenName': 'Pera87', 'country_name': 'Japan',
    #                                   'citizenAvatar': 'https://cdnt.erepublik.net/epJxfzXbIXZNXmPxHzXQJiRUeMg=/30x30/smart/avatars/Citizens/2011/03/16/d95fa2738eb2c9a4a8756e5eea9f9aff.jpg?8b868280fe873e90a8a13842ae57e125',
    #                                   'country_permalink': 'Japan', 'for_country_id': 45, 'value': '3,289,026',
    #                                   'raw_value': 3289026, 'reward': False}}, 'pages': 0}}

    ret = []
    for country_id, data in resp.items():
        # print(" country id:" , country_id)
        if not int(country_id) == player.details.citizenship:
            continue
        try:
            for place in sorted(data.get("fighterData", {}).values(), key=lambda _: -_['raw_value']):
                ret.append((place['citizenName'], place['citizenId'], place['raw_value']))
        except:
            continue
    place = -1
    # print("name: ", self.name)
    print("get_hit_status ret ", ret)
    if len(ret) == 0:
        return 0
    for fighter in ret:
        if division == 1:
            if fighter[1] in target_hit:
                if fighter[2] < 5000000:
                    place = ret.index(fighter) + 1
                    return place
        if division == 2:
            if fighter[1] in target_hit:
                if fighter[2] < 5000000:
                    place = ret.index(fighter) + 1
                    return place
        if division == 3:
            if fighter[1] in target_hit:
                if fighter[2] < 5000000:
                    place = ret.index(fighter) + 1
                    return place
    return place


def get_my_status_only(player: Citizen, battle_id: int, div: int = 4):
    # return {}
    battle = player.all_battles.get(battle_id)
    print("2931")
    round_id = battle.zone_id
    division = div if round_id % 4 > 0 else 11
    division = div
    resp = player._post_military_battle_console(battle_id, 'battleStatistics', round_id=round_id,
                                                division=division).json()
    resp.pop('rounds', None)
    # {'14': {'fighterData': {'1': {'citizenId': 1542079, 'citizenName': 'jiqimaono2', 'country_name': 'China',
    #                               'citizenAvatar': 'https://cdnt.erepublik.net/7s5Qg3dx1IiFOtYYGRa3yJK8URM=/30x30/smart/avatars/Citizens/2009/06/11/820af46e7726ab11dd955c73954a22e0.jpg',
    #                               'country_permalink': 'China', 'for_country_id': 14, 'value': '14,358,582',
    #                               'raw_value': 14358582, 'reward': False},
    #                         '2': {'citizenId': 5368708, 'citizenName': 'Legen017', 'country_name': 'Spain',
    #                               'citizenAvatar': 'https://cdnt.erepublik.net/OAGxWEnN2unJA6xViZIX5UKVg-Q=/30x30/smart/avatars/Citizens/2011/11/23/a0c1f09662432ea6a9ec0a5d6f0d2015.jpg?a76e9aa274a07715d40d260ae3042f62',
    #                               'country_permalink': 'Spain', 'for_country_id': 14, 'value': '847,617',
    #                               'raw_value': 847617, 'reward': False}}, 'pages': 0}, '45': {'fighterData': {
    #     '1': {'citizenId': 4080491, 'citizenName': 'MisterTerminator', 'country_name': 'Japan',
    #           'citizenAvatar': 'https://cdnt.erepublik.net/RVjn9scT7VjWJXmL4ZiiZGlIGvA=/30x30/smart/avatars/Citizens/2010/11/14/38296b897dbf99d9a4c4279bdc865cd9.jpg?c858079a0ff17f1a0bf7d0bf9e7facee',
    #           'country_permalink': 'Japan', 'for_country_id': 45, 'value': '18,760,980', 'raw_value': 18760980,
    #           'reward': False}, '2': {'citizenId': 4580613, 'citizenName': 'Pera87', 'country_name': 'Japan',
    #                                   'citizenAvatar': 'https://cdnt.erepublik.net/epJxfzXbIXZNXmPxHzXQJiRUeMg=/30x30/smart/avatars/Citizens/2011/03/16/d95fa2738eb2c9a4a8756e5eea9f9aff.jpg?8b868280fe873e90a8a13842ae57e125',
    #                                   'country_permalink': 'Japan', 'for_country_id': 45, 'value': '3,289,026',
    #                                   'raw_value': 3289026, 'reward': False}}, 'pages': 0}}

    ret = []
    for country_id, data in resp.items():
        # print(" country id:" , country_id)
        if not int(country_id) == 14:
            continue
        try:
            for place in sorted(data.get("fighterData", {}).values(), key=lambda _: -_['raw_value']):
                ret.append((place['citizenName'], place['citizenId'], place['raw_value']))
        except:
            continue
    place = -1
    dam = 0
    # print("name: ", self.name)
    if len(ret) == 0:
        max = 0
        return place, dam, max
    else:
        max = ret[0][2]
    for fighter in ret:
        # if fighter[1] == self.details.citizen_id:
        if fighter[1] == player.details.citizen_id:
            place = ret.index(fighter) + 1
            dam = fighter[2]
        # elif fighter[0] == 'xtt1230':
        #     place = ret.index(fighter) + 1
    return place, dam, max


def find_avaiable_hits(player: Citizen, battles2, battles, div=[1, 2, 3, ], localonly: bool = True,
                       findempty: bool = True):
    print("find_avaiable_hits util.now: ", utils.now())
    print("find_avaiable_hits found: ", battles)
    dmg1 = {1: 5500000, 2: 11500000, 3: 15500000}
    dmg2 = {1: 7500000, 2: 13500000, 3: 17000000}
    for id in battles:
        print("find_avaiable_hits found: ", player.all_battles[id])
        for i in range(1, 4):
            place = get_hit_status(player, id, div=i)
            time.sleep(2)
            if not findempty:
                if not place == 1:
                    continue
            else:
                if not place == 0:
                    continue
            return id, i, dmg1[i]
    time.sleep(2)
    if not localonly:
        battles_allground = [item for item in battles2 if item not in battles]
        print("find_avaiable_hits battles allground found: ", battles_allground)
        for id in battles_allground:
            print(player.all_battles[id])
            for i in range(1, 4):
                place = get_hit_status(id, div=i)
                time.sleep(2)
                if not findempty:
                    if not place == 1:
                        continue
                else:
                    if not place == 0:
                        continue
                return id, i, dmg2[i]
    if len(battles) > 0:
        maxdamage = 1000000000
        index = 0
        for id in battles:
            print("find_avaiable_hits 451")
            place, mydam, max = get_my_status_only(id, div=4)
            print("find_avaiable_hits 453")
            print("max: {} my damage {}:".format(max, mydam))
            if max - mydam < maxdamage:
                maxdamage = max - mydam
                index = battles.index(id)

        return battles[index], 4, 0
    elif len(battles_allground) > 0 and not localonly:
        maxdamage = 1000000000
        index = 0
        for id in battles_allground:
            place, mydam, max = get_my_status_only(id, div=4)
            # max = player.get_my_status_damage(id, div=4)
            max = get_my_status_only(player,id,div=4)[1]
            print("max: {} my damage {}:".format(max, mydam))
            if max - mydam < maxdamage:
                maxdamage = max - mydam
                index = battles.index(id)
        return battles_allground[index], 4, 0
    return 0, 0, 0


def find_avaiable_hits_did(player: Citizen, battles2, battles, localonly: bool = False,
                           findempty: bool = True):
    player.update_war_info()
    print("find_avaiable_hits_did util: ", utils.now())
    dmg1 = {1: 5100000, 2: 11100000, 3: 13100000}
    dmg2 = {1: 7200000, 2: 13200000, 3: 17200000}
    print(dmg1[1])
    for id in battles:
        print(player.all_battles[id])
        delta = utils.now() - player.all_battles[id].start
        if (delta > timedelta(minutes=45) or delta < timedelta(minutes=0)):
            continue
        for i in range(1, 4):
            place = get_hit_status(id, div=i)
            time.sleep(2)
            if not findempty:
                if not place == 1:
                    continue
                else:
                    return id, i, dmg1[i]
            if findempty:
                if not place == 0:
                    continue
                else:
                    return id, i, dmg1[i]
    time.sleep(2)
    if not localonly:
        print("battles allground found: ", battles2)
        battles_allground = [item for item in battles2 if item not in battles]
        print("battles allground found: ", battles_allground)
        for id in battles_allground:
            print(player.all_battles[id])
            delta = utils.now() - player.all_battles[id].start
            if (delta > timedelta(minutes=45) or delta < timedelta(minutes=0)):
                continue
            for i in range(1, 4):
                place = get_hit_status(id, div=i)
                time.sleep(2)
                if not findempty:
                    if not place == 1:
                        continue
                    else:
                        return id, i, dmg2[i]
                if findempty:
                    if not place == 0:
                        continue
                    else:
                        return id, i, dmg2[i]
    return 0, 0, 0


def find_avaiable_hits_di_d1_3(player: Citizen, battles2, battles, div=[1, 2, 3, 4], localonly: bool = True,
                               findempty: bool = False):
    player.update_war_info()
    print("find_avaiable_hits_di_d1_3 util: ", utils.now())
    dmg1 = {1: 5100000, 2: 11100000, 3: 13100000}
    dmg2 = {1: 7200000, 2: 13200000, 3: 17000000}
    for id in battles:
        print("find_avaiable_hits_di_d1_3 462 ", player.all_battles[id])
        delta = utils.now() - player.all_battles[id].start
        if (delta > timedelta(minutes=45) or delta < timedelta(minutes=0)):
            continue
        print("find_avaiable_hits_di_d1_3 466 delta: ", delta)
        place1 = get_hit_status(player, id, div=1)
        place2 = get_hit_status(player, id, div=2)
        place3 = get_hit_status(player, id, div=3)
        for i in range(4, 15):
            print("find_avaiable_hits_di_d1_3 range: ", i, " ", get_hit_status(player, id, div=i))
        print("find_avaiable_hits_di_d1_3 537 place: {}/{}/{} ".format(place1, place2, place3))
        if not findempty:
            if place1 == 1 and place2 == 1 and place3 == 1:
                return id, 123, dmg1
            elif place2 == 1 and place3 == 1:
                return id, 23, dmg1
            elif place1 == 1 and place2 == 1:
                return id, 12, dmg1
            elif place1 == 1:
                return id, 1, dmg1
            elif place2 == 1:
                return id, 2, dmg1
            elif place3 == 1:
                return id, 3, dmg1
        else:
            if place1 == 0 and place2 == 0 and place3 == 0:
                return id, 123, dmg1
            elif place2 == 0 and place3 == 0:
                return id, 23, dmg1
            elif place1 == 0 and place2 == 0:
                return id, 12, dmg1
            elif place1 == 0:
                return id, 1, dmg1
            elif place2 == 0:
                return id, 0, dmg1
            elif place3 == 0:
                return id, 3, dmg1
    time.sleep(2)
    if not localonly:
        battles_allground = [item for item in battles2 if item not in battles]
        print("battles allground found: ", battles_allground)
        for id in battles_allground:
            print(player.all_battles[id])
            delta = utils.now() - player.all_battles[id].start
            print(delta)
            if (delta > timedelta(minutes=55)):
                print("skip!")
                continue
            place1 = get_hit_status(player, id, div=1)
            place2 = get_hit_status(player, id, div=2)
            place3 = get_hit_status(player, id, div=3)
            if not findempty:
                if place1 == 1 and place2 == 1 and place3 == 1:
                    return id, 123, dmg2
                elif place2 == 1 and place3 == 1:
                    return id, 23, dmg2
                elif place1 == 1 and place2 == 1:
                    return id, 12, dmg2
                elif place1 == 1:
                    return id, 1, dmg2
                elif place2 == 1:
                    return id, 2, dmg2
                elif place3 == 1:
                    return id, 3, dmg2
            else:
                if place1 == 0 and place2 == 0 and place3 == 0:
                    return id, 123, dmg2
                elif place2 == 0 and place3 == 0:
                    return id, 23, dmg2
                elif place1 == 0 and place2 == 0:
                    return id, 12, dmg2
                elif place1 == 0:
                    return id, 1, dmg2
                elif place2 == 0:
                    return id, 0, dmg2
                elif place3 == 0:
                    return id, 3, dmg2
    return 0, 0, 0


def _battle_monitor_hit(player: Citizen, hrs: float):
    """Launch battles. Check every 5th minute (0,5,10...45,50,55) if any battle could be started on specified regions
    and after launching wait for 90 minutes before starting next attack so that all battles aren't launched at the same
    time. If player is allowed to fight, do 100 hits on the first round in players division.

    :param player: Logged in Citizen instance
    ":type player: Citizen
    """
    global CONFIG
    finished_war_ids = {*[]}
    war_data = CONFIG.get('start_battles', {})
    next_attack_time = player.now
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=59)
    print("hit 101", next_attack_time)
    bh_watch_list = []
    new_battle_list = []
    while not player.stop_threads.is_set():
        try:
            ####################################################################
            player.update_citizen_info()
            player.update_inventory()
            print(player.energy)
            print("hrs: ", hrs)
            # print("missing energy: ", player.energy.limit * 2 - player.energy.available)
            # print("consider-full energy: ", player.energy.limit * 2 - hrs * 10 * player.energy.interval)
            print("consider-full time: ",
                  (player.energy.limit * 2 - player.energy.available) / (10 * player.energy.interval))
            # energy.limit: 1060  energy.recoverable: 769 energy.recovered: 1060 energy.available: 1829 energy.interval: 30
            print(player.food)
            if not player.is_levelup_reachable:
                print(player.eat())
            if ((player.energy.limit * 2 - player.energy.available < int(hrs * 10 * player.energy.interval)) and
                (player.energy.available > 600)):
                hit, div, dam = find_avaiable_hits(player)
                # hit, div, dam = find_avaiable_hits_did(player)
                print("hit, div, dam: {} {} {} ".format(hit, div, dam))
                if hit > 0:
                    print("lets hit")
                    player.fight_until_damage(hit, player.details.citizenship, count=int(0.1 * player.energy.interval),
                                              division=div, damage_final=dam)
                    # player.fight_until_damage(hit, player.details.citizenship, count=1,
                    #                           division=div, damage_final=dam)
                else:
                    print("no avaiable battle! ")
                if not player.is_levelup_reachable:
                    print(player.eat())
            if not player.details.current_region == player.details.residence_region:
                player.travel_to_region(player.details.residence_region)

            ######################################################################
            player.update_war_info()
            print("1")
            battles = player.cus_sorted_battles()
            for id in battles:
                print(player.all_battles[id])
                delta = utils.now() - player.all_battles[id].start
                if (delta < timedelta(minutes=12) and
                    delta > timedelta(minutes=0)):
                    print("found!")
                    newbattleinfo = str(id) + ":" + str(player.all_battles[id].zone_id)
                    print(newbattleinfo)
                    if not newbattleinfo in new_battle_list:
                        # message = 'find battle: ' + str(player.all_battles[id])
                        message2 = '/hit 123 https://www.erepublik.com/en/military/battlefield/' + str(id) + ' cn '
                        message3 = " new battle:  " + str(delta)
                        message4 = 'https://www.erepublik.com/en/military/battlefield/' + str(id)
                        # post(player.telegram.api_url,json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                        # post(player.telegram.api_url,
                        #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                        # post(player.telegram.api_url,
                        #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                        telextt(message2)
                        if (not player.all_battles[id].is_rw) and player.energy.available > 1000:
                            post(player.telegram.api_url,
                                 json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                        new_battle_list.append(newbattleinfo)
                        # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                        # continue

                if (delta > timedelta(minutes=71)):
                    for i in range(1, 4):
                        bh_watch = str(id) + ":" + str(player.all_battles[id].zone_id) + ":" + str(i)
                        if bh_watch in bh_watch_list:
                            continue
                        place = player.get_my_status(id, div=i)
                        if place > 1:
                            print(bh_watch)
                            if not bh_watch in bh_watch_list:
                                message = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                                          + "  check BH in Div: " + str(i)
                                post(player.telegram.api_url,
                                     json=dict(chat_id=player.telegram.chat_id, text=message, parse_mode="Markdown"))
                                telextt(message)
                                print(message)
                            bh_watch_list.append(bh_watch)
                        else:
                            print("check BH done: ", "div ", i, place)
                    time.sleep(2)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except Exception as inst:
            print("hit except", inst)
            player.report_error("Task error: start_battles")
        ###########################################################
        # over_time, train, buy offer
        ##########################################
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=300))
        print("hit 149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))


def _battle_monitor_after_summer(player: Citizen, hrs: float):
    #inherit from _battle_monitor_hit
    """Launch battles. Check every 5th minute (0,5,10...45,50,55) if any battle could be started on specified regions
    and after launching wait for 90 minutes before starting next attack so that all battles aren't launched at the same
    time. If player is allowed to fight, do 100 hits on the first round in players division.

    :param player: Logged in Citizen instance
    ":type player: Citizen
    """
    global CONFIG
    finished_war_ids = {*[]}
    war_data = CONFIG.get('start_battles', {})
    next_attack_time = player.now
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=59)
    print("hit 101", next_attack_time)
    bh_watch_list = []
    new_battle_list = []
    while not player.stop_threads.is_set():
        try:
            ####################################################################
            # player.update_citizen_info()
            # player.update_inventory()
            # print(player.energy)
            # print("hrs: ", hrs)
            # # print("missing energy: ", player.energy.limit * 2 - player.energy.available)
            # # print("consider-full energy: ", player.energy.limit * 2 - hrs * 10 * player.energy.interval)
            # print("consider-full time: ",
            #       (player.energy.limit * 2 - player.energy.available) / (10 * player.energy.interval))
            # # energy.limit: 1060  energy.recoverable: 769 energy.recovered: 1060 energy.available: 1829 energy.interval: 30
            # print(player.food)
            # if not player.is_levelup_reachable:
            #     print(player.eat())
            # if ((player.energy.limit * 2 - player.energy.available < int(hrs * 10 * player.energy.interval)) and
            #     (player.energy.available > 600)):
            #     hit, div, dam = find_avaiable_hits(player)
            #     # hit, div, dam = find_avaiable_hits_did(player)
            #     print("hit, div, dam: {} {} {} ".format(hit, div, dam))
            #     if hit > 0:
            #         print("lets hit")
            #         # player.fight_until_damage(hit, player.details.citizenship, count=int(0.1 * player.energy.interval),
            #         #                           division=div, damage_final=dam)
            #         after_summer_fight(player, id, count=1)
            #         # player.fight_until_damage(hit, player.details.citizenship, count=1,
            #         #                           division=div, damage_final=dam)
            #     else:
            #         print("no avaiable battle! ")
            #     if not player.is_levelup_reachable:
            #         print(player.eat())
            # if not player.details.current_region == player.details.residence_region:
            #     player.travel_to_region(player.details.residence_region)

            ######################################################################
            #below from summer
            player.update_war_info()
            battles_list = cus_sorted_battles(player)
            battles = battles_list[4] # all ground battle
            battlesall = battles_list[3]
            # guaji_fangti(player, hrs, battlesall, battles)
            utils.now()
            new_battle_list,bh_watch_list = inform_new_and_checkBH(player,battles,new_battle_list,bh_watch_list)
            player.update_citizen_info()
            if not player.details.current_region == player.details.residence_region:
                print("player.details.current_region", player.details.current_region)
                print("player.details.residence_region", player.details.residence_region)
                # player.travel_to_region(player.details.residence_region)
                player.travel_to_residence()
                data = {
                    "toCountryId": 14,
                    "inRegionId": 395,
                }
                player._post_main_travel("moveAction", **data)
                # player.travel_to_holding(player.my_companies.holdings[0])
            print("_battle_monitor 811",battles)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except Exception as inst:
            print("hit except", inst)
            player.report_error("Task error: start_battles")
        ###########################################################
        # over_time, train, buy offer
        ##########################################
        # work_train_buy_eat(player)
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=300))
        print("hit 149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))


def _battle_monitor_hit_zaixian(player: Citizen, hrs: float):
    """hit when have full energy

    :param player: Logged in Citizen instance
    ":type player: Citizen
    """
    global CONFIG
    finished_war_ids = {*[]}
    war_data = CONFIG.get('start_battles', {})
    next_attack_time = player.now
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=59)
    print("hit 101", next_attack_time)
    bh_watch_list = []
    new_battle_list = []
    while not player.stop_threads.is_set():
        # ##########################################################################
        player.update_citizen_info()
        player.update_inventory()
        print(player.energy)
        print("hrs: ", hrs)
        print("consider-full time: ",
              (player.energy.limit * 2 - player.energy.available) / (10 * player.energy.interval))
        # energy.limit: 1060  energy.recoverable: 769 energy.recovered: 1060 energy.available: 1829 energy.interval: 30
        print(player.food)
        if not player.is_levelup_reachable:
            print(player.eat())
        # print("missing energy: ",player.energy.limit * 2 - player.energy.available)
        # print("consider-full energy: ",player.energy.limit * 2 - hrs * 10 * player.energy.interval)
        for i in range(1, 4):
            if (player.energy.available > 500):
                hit, div, dam = find_avaiable_hits_di_d1_3(player)
                print("hit, div, dam: {} {} {} ".format(hit, div, dam))
                if hit > 0:
                    player.activate_dmg_booster()
                    if div == 123 or div == 12 or div == 13 or div == 1:
                        print("lets hit 1")
                        player.fight_until_damage(hit, player.details.citizenship,
                                                  count=int(0.5 * player.energy.interval),
                                                  division=1, damage_final=dam[1])
                        time.sleep(2)
                    if div == 123 or div == 12 or div == 23 or div == 2:
                        print("lets hit 2")

                        player.fight_until_damage(hit, player.details.citizenship,
                                                  count=int(0.5 * player.energy.interval),
                                                  division=2, damage_final=dam[2])
                        time.sleep(2)
                    if div == 123 or div == 23 or div == 13 or div == 3:
                        print("lets hit 3")

                        player.fight_until_damage(hit, player.details.citizenship,
                                                  count=int(0.5 * player.energy.interval),
                                                  division=3, damage_final=dam[3])
                        time.sleep(2)
                    messagehit = 'https://www.erepublik.com/en/military/battlefield/' + str(hit) \
                                 + "  hit done for zaixian: div: " + str(div)
                    post(player.telegram.api_url,
                         json=dict(chat_id=player.telegram.chat_id, text=messagehit, parse_mode="Markdown"))
                    # player.fight_until_damage(hit, player.details.citizenship, count=1,
                    #                           division=div, damage_final=dam)
                else:
                    print("no avaiable battle! ")
                if not player.is_levelup_reachable:
                    print(player.eat())
                time.sleep(10)
        if not player.details.current_region == player.details.residence_region:
            player.travel_to_region(player.details.residence_region)
        #######################################################################################
        try:
            player.update_war_info()
            print("1")
            battles = player.cus_sorted_battles()
            for id in battles:
                print(player.all_battles[id])
                delta = utils.now() - player.all_battles[id].start
                if (delta < timedelta(minutes=15) and
                    delta > timedelta(minutes=0)):
                    print("found!")
                    newbattleinfo = str(id) + ":" + str(player.all_battles[id].zone_id)
                    print(newbattleinfo)
                    if not newbattleinfo in new_battle_list:
                        # message = 'find battle: ' + str(player.all_battles[id])
                        message2 = '/hit 123 https://www.erepublik.com/en/military/battlefield/' + str(id) + ' cn '
                        message3 = " new battle:  " + str(delta)
                        message4 = 'https://www.erepublik.com/en/military/battlefield/' + str(id)
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                        # post(player.telegram.api_url,
                        #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                        # post(player.telegram.api_url,
                        #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                        telextt(message2)
                        new_battle_list.append(newbattleinfo)
                        # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                        # continue

                if (delta > timedelta(minutes=71)):
                    for i in range(1, 4):
                        bh_watch = str(id) + ":" + str(player.all_battles[id].zone_id) + ":" + str(i)
                        if bh_watch in bh_watch_list:
                            continue
                        place = player.get_my_status(id, div=i)
                        if place > 1:
                            print(bh_watch)
                            if not bh_watch in bh_watch_list:
                                message = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                                          + "  check BH in Div: " + str(i)
                                post(player.telegram.api_url,
                                     json=dict(chat_id=player.telegram.chat_id, text=message, parse_mode="Markdown"))
                                telextt(message)
                                print(message)
                            bh_watch_list.append(bh_watch)
                        else:
                            print("check BH done: ", "div ", i, place)
                    time.sleep(2)

            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except Exception as inst:
            print("hit except", inst)
            player.report_error("Task error: start_battles")
        ###########################################################
        # over_time, train, buy offer
        ##########################################
        try:

            player.work()
            player.train()
            player.collect_weekly_reward()
            # player.buy_monetary_market_offer()
            ################################################
            print("1")
            next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=240))
            print("hit 149", next_attack_time)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except Exception as inst:
            print("hit except", inst)
            player.report_error("Task error: start_battles")


def cus_sorted_battles(player: Citizen, sort_by_time: bool = True) -> List[List[int]]:
    cs_battles_priority_air: List[int] = []
    cs_battles_priority_ground: List[int] = []
    cs_battles_air: List[int] = []
    cs_battles_ground: List[int] = []
    deployed_battles_air: List[int] = []
    deployed_battles_ground: List[int] = []
    ally_battles_air: List[int] = []
    ally_battles_ground: List[int] = []
    other_battles_air: List[int] = []
    other_battles_ground: List[int] = []
    cs_battles_ground_not_rw: List[int] = []

    ret_battles: List[int] = []
    if sort_by_time:
        battle_list = sorted(player.all_battles.values(), key=lambda b: b.start)
        battle_list.reverse()
    else:
        battle_list = sorted(player.all_battles.values(), key=lambda b: b.id)

    contribution_json: Response = player._get_military_campaigns_json_citizen()
    contributions: List[Dict[str, int]] = contribution_json.json().get('contributions') or []
    contributions.sort(key=lambda b: -b.get('damage'))
    ret_battles += [int(b.get('battle_id', 0)) for b in contributions if b.get('battle_id')]

    for battle in battle_list:
        battle_sides = [battle.invader.id, battle.defender.id]
        if battle.id in ret_battles:
            continue
        # CS Battles
        elif player.details.citizenship in battle_sides:
            if not battle.is_rw:
                cs_battles_ground_not_rw.append(battle.id)
            if battle.has_air:
                if battle.defender.id == player.details.citizenship:
                    cs_battles_priority_air.append(battle.id)
                else:
                    cs_battles_air.append(battle.id)
            else:
                if battle.defender.id == player.details.citizenship:
                    cs_battles_priority_ground.append(battle.id)
                else:
                    cs_battles_ground.append(battle.id)

        # Current location battles:
        elif player.details.current_country in battle_sides:
            if battle.has_air:
                deployed_battles_air.append(battle.id)
            else:
                deployed_battles_ground.append(battle.id)

        # Deployed battles and allied battles:
        elif player.details.current_country in battle.invader.allies + battle.defender.allies + battle_sides:
            if player.details.current_country in battle.invader.deployed + battle.defender.deployed:
                if battle.has_air:
                    deployed_battles_air.append(battle.id)
                else:
                    deployed_battles_ground.append(battle.id)
            # Allied battles:
            else:
                if battle.has_air:
                    ally_battles_air.append(battle.id)
                else:
                    ally_battles_ground.append(battle.id)
        else:
            if battle.has_air:
                other_battles_air.append(battle.id)
            else:
                other_battles_ground.append(battle.id)

    cs_battles = cs_battles_priority_air + cs_battles_priority_ground + cs_battles_air + cs_battles_ground
    deployed_battles = deployed_battles_air + deployed_battles_ground
    other_battles = ally_battles_air + ally_battles_ground + other_battles_air + other_battles_ground
    ret_battles = ret_battles + cs_battles + deployed_battles + other_battles
    return [cs_battles_priority_air, cs_battles_priority_ground, cs_battles_air, cs_battles_ground,
            cs_battles_ground_not_rw,
            deployed_battles_air, deployed_battles_ground,
            ally_battles_air, ally_battles_ground, other_battles_air, other_battles_ground
            ]


def get_my_status(player: Citizen, battle_id: int, div: int = 4) -> int:
    # return {}
    battle = player.all_battles.get(battle_id)
    round_id = battle.zone_id
    division = div if round_id % 4 > 0 else 11
    resp = player._post_military_battle_console(battle_id, 'battleStatistics', round_id=round_id,
                                                division=division).json()
    resp.pop('rounds', None)
    ret = []
    # print(resp)
    for country_id, data in resp.items():
        # print(" country id:" , country_id)
        if not int(country_id) == 14:
            continue
        try:
            for place in sorted(data.get("fighterData", {}).values(), key=lambda _: -_['raw_value']):
                ret.append((place['citizenName'], place['citizenId'], place['raw_value']))
        except:
            continue
    place = -1
    # print("name: ", self.name)
    if len(ret) == 0:
        return place
    for fighter in ret:
        if fighter[1] == player.details.citizen_id:
            # if fighter[1] == 1542079:
            place = ret.index(fighter) + 1
            return place
        elif fighter[0] == 'xtt1230':
            place = ret.index(fighter) + 1
            return place
    return place


def main():
    player = Citizen(email=CONFIG['email'], password=CONFIG['password'], auto_login=False)
    player.config.interactive = CONFIG['interactive']
    player.config.fight = CONFIG['fight']
    player.config.telegram_chat_id = CONFIG['telegram_chat_id']
    player.config.telegram_token = CONFIG['telegram_token']
    player.set_debug(CONFIG.get('debug', False))
    player.login()

    id = 300918
    # player.update_war_info()
    player.update_all()
    player.update_war_info()
    battles_list = cus_sorted_battles(player)
    battles = battles_list[4]  # all ground battle
    battlesall = battles_list[3]
    #
    # for int in range(1,4):
    #     place = get_hit_status(player,id,int)
    #     print(place)
    # hit, div, dam = find_avaiable_hits_di_d1_3(player, battlesall, battles, findempty=True)
    # print("guaji_fangti hit, div, dam: {} {} {} ".format(hit, div, dam))
    # hit, div, dam = find_avaiable_hits(player, battlesall, battles, findempty=True)
    # print("guaji_fangti 2  hit, div, dam: {} {} {} ".format(hit, div, dam))
    #
    # hit, div, dam = find_avaiable_hits_di_d1_3(player, battlesall, battles, findempty=True)
    # print("guaji_fangti hit, div, dam: {} {} {} ".format(hit, div, dam))
    # if hit > 0:
    #     print("lets hit")
    #     # player.fight(hit, div, player.details.citizenship, count=1)
    #     after_summer_fight_div(player, hit, div)
    #     # player.fight_until_damage(hit, player.details.citizenship, count=1,
    #     #                           division=div, damage_final=dam)
    # else:
    #     hit, div, dam = find_avaiable_hits(player, battlesall, battles, findempty=True)
    #     print("guaji_fangti hit, div, dam: {} {} {} ".format(hit, div, dam))
    #     if hit > 0:
    #         print("lets hit")
    #         # player.fight(hit, div, player.details.citizenship, count=1)
    #         after_summer_fight_div(player, hit, div)
    #         # player.fight_until_damage(hit, player.details.citizenship, count=1,
    #         #                           division=div, damage_final=dam)
    #     print("no avaiable battle! ")

    # battles_list = cus_sorted_battles(player)
    # return [cs_battles_priority_air,
    # cs_battles_priority_ground,
    # cs_battles_air,
    # cs_battles_ground,
    #         cs_battles_ground_not_rw,
    #         deployed_battles_air,
    #         deployed_battles_ground,
    #         ally_battles_air, ally_battles_ground, other_battles_air, other_battles_ground
    #         ]
    # battle0 = battles_list[0]
    # battles1 = battles_list[4]
    # for i in range(0,7):
    #     print(i)
    #     print(battles_list[i])

    ############################################################################    ####################################################################
    # guaji-after summer - auto find local d123 to hit and hit d4 if energy is almost full,
    ##################################################
    # hrs: float = 0.6
    # # hrs: float = 4
    # name = "{}-start_battles_moniter_hit-{}".format(player.name, threading.active_count() - 1)
    # state_thread = threading.Thread(target=_battle_monitor_after_summer, args=(player, hrs), name=name)
    # state_thread.start()
    ############################################################################

    ####################################################################
    # zaixian - auto find d123 to hit, if energy is almost full,
    ##################################################
    # hrs: float = 0.6
    # # hrs: float = 4
    # name = "{}-start_battles_moniter_hit_zaixian-{}".format(player.name, threading.active_count() - 1)
    # state_thread = threading.Thread(target=_battle_monitor_hit_zaixian, args=(player, hrs), name=name)
    # state_thread.start()
    ############################################################################


if __name__ == "__main__":
    main()

    # print(utils.now())
    # print(utils.now().hour)
    # msg = "/profile"
    # msg = "/hit 3 https://www.erepublik.com/en/military/battlefield/280650 cn"
    # xtttoken = '1255503748:AAGKqHbDh_SkZoFgTHE_761li730EMu8OYo'
    # xtttoken = '1062108968:AAGRkXhOpA9qTuQ0Se8YFY0JnrKwImH_F4k'
    # xttid = -1496901954
    # xttid = 1271891790
    # api_url = "https://api.telegram.org/bot{}/sendMessage".format(xtttoken)
    # print(api_url)
    # post(api_url,
    #      json=dict(chat_id=xttid, text=msg, parse_mode="Markdown"))

    # ret = []
    # ret.append(('birdoffire', 1802652, 96131666))
    # ret.append(('Goran Brkic', 1445080, 72931659))
    # print(ret)
    # print(ret[0][0])
    # print(ret[1])

    # msg = 'test2'
    # telextt(msg)

    # dmg1 = {1: 5500000, 2: 11500000, 3:15500000}
    # dmg1 = {1: 7500000, 2: 13500000, 3:17000000}
    # print(dmg1[1])
