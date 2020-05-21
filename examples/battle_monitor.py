import threading
import time

from requests import Response, Session, post

from datetime import timedelta

from erepublik import Citizen, utils

CONFIG = {
    'email': '',
    'password': '',
    'interactive': True,
    'fight': False,
    'debug': True,
    'start_battles': {
        121672: {"auto_attack": False, "regions": [661]},
        125530: {"auto_attack": False, "regions": [259]},
        125226: {"auto_attack": True, "regions": [549]},
        124559: {"auto_attack": True, "regions": [176]}
    },
    'telegram_chat_id': '',
    'telegram_token': ''
}


def _battle_launcher(player: Citizen):
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
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=0)
    while not player.stop_threads.is_set():
        try:
            attacked = False
            player.update_war_info()
            running_wars = {b.war_id for b in player.all_battles.values()}
            for war_id in war_ids - finished_war_ids - running_wars:
                war = war_data[str(war_id)]
                war_regions = set(war.get('regions'))
                auto_attack = war.get('auto_attack')

                status = player.get_war_status(war_id)
                if status.get('ended', False):
                    CONFIG['start_battles'].pop(str(war_id), None)
                    finished_war_ids.add(war_id)
                    continue
                elif not status.get('can_attack'):
                    continue

                if auto_attack or (player.now.hour > 20 or player.now.hour < 2):
                    for reg in war_regions:
                        if attacked:
                            break
                        if reg in status.get('regions', {}).keys():
                            player.launch_attack(war_id, reg, status.get('regions', {}).get(reg))
                            attacked = True
                            hits = 100
                            if player.energy.food_fights >= hits and player.config.fight:
                                for _ in range(120):
                                    player.update_war_info()
                                    battle_id = player.get_war_status(war_id).get("battle_id")
                                    if battle_id is not None and battle_id in player.all_battles:
                                        player.fight(battle_id, player.details.citizenship, hits)
                                        break
                                    player.sleep(1)
                        if attacked:
                            break
                if attacked:
                    break
            war_ids -= finished_war_ids
            if attacked:
                next_attack_time = utils.good_timedelta(next_attack_time, timedelta(hours=1, minutes=30))
            else:
                next_attack_time = utils.good_timedelta(next_attack_time, timedelta(minutes=5))
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except:
            player.report_error("Task error: start_battles")

def _battle_monitor_air(player: Citizen):
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
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=0)
    print("101",next_attack_time)
    new_battle_list = []
    bh_watch_list = []
    while not player.stop_threads.is_set():
        try:
            player.update_war_info()
            battles = player.cus_sorted_battles_all_air()
            print(battles)
            utils.now()
            for id in battles:
                delta = utils.now() - player.all_battles[id].start
                time.sleep(1)
                print(delta)
                if (delta < timedelta(minutes=0)):
                    print("found!")
                    newbattleinfo = str(id)+ ":"+ str(player.all_battles[id].zone_id)
                    print(newbattleinfo)
                    if not newbattleinfo in new_battle_list:
                        # message = 'find battle: ' + str(player.all_battles[id])
                        message2 = 'https://www.erepublik.com/en/military/battlefield/' + str(id)
                        message3 = " new battle:  " + str(delta)
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                        new_battle_list.append(newbattleinfo)
                        # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                        continue
            print(battles)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except:
            player.report_error("Task error: start_battles")
        ###########################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(minutes=3))
        print("133", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))

def _battle_monitor_all(player: Citizen):
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
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=0)
    print("101",next_attack_time)
    new_battle_list = []
    while not player.stop_threads.is_set():
        player.update_war_info()
        battles = player.cus_sorted_battles_all_groud()
        print(battles)
        for id in battles:
            delta = utils.now() - player.all_battles[id].start
            time.sleep(2)
            if (delta > timedelta(minutes=70)):
                # print("found!")
                newbattleinfo = str(id)+ ":"+ str(player.all_battles[id].zone_id)
                print(newbattleinfo)
                # if not newbattleinfo in new_battle_list:
                #     # message = 'find battle: ' + str(player.all_battles[id])
                #     message2 = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                #                + " new battle:  " + str(delta)
                #     post(player.telegram.api_url,
                #          json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                #     new_battle_list.append(newbattleinfo)
                #     # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                #     continue
                for i in range(1,5) :
                    place = player.get_empty_status(id, div=i)
                    print(place)
                    time.sleep(1)
                    if place > 0:
                        message = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                                  + "  empty in Div: " + str(i)
                        post(player.telegram.api_url, json=dict(chat_id=player.telegram.chat_id, text=message, parse_mode="Markdown"))
                        print(message)
                        break
                    else:
                        print("check BH done: ", "div ", i, place)

        print(battles)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        ###########################################################
        # over_time
        # player.update_job_info()
        # ot_time = player.my_companies.next_ot_time
        # delta = utils.now() - ot_time
        # print(" next overtime", delta)
        # if delta > timedelta(minutes=1):
        #     player.work_ot()
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(minutes=5))
        print("149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))


def _battle_monitor(player: Citizen):
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
    next_attack_time = next_attack_time.replace(minute=next_attack_time.minute // 5 * 5, second=0)
    print("101",next_attack_time)
    new_battle_list = []
    bh_watch_list = []
    while not player.stop_threads.is_set():
        try:
            player.update_war_info()
            battles = player.cus_sorted_battles()
            utils.now()
            for id in battles:
                print(player.all_battles[id])
                delta = utils.now() - player.all_battles[id].start
                time.sleep(2)
                if (delta < timedelta(minutes=5) and
                    delta > timedelta(minutes=-2)):
                    print("found!")
                    newbattleinfo = str(id)+ ":"+ str(player.all_battles[id].zone_id)
                    print(newbattleinfo)
                    if not newbattleinfo in new_battle_list:
                        # message = 'find battle: ' + str(player.all_battles[id])
                        message2 = '/hit 2 https://www.erepublik.com/en/military/battlefield/' + str(id) + ' cn '
                        message3 = " new battle:  " + str(delta)
                        message4 ='https://www.erepublik.com/en/military/battlefield/' + str(id)
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message2, parse_mode="Markdown"))
                        post(player.telegram.api_url,
                             json=dict(chat_id=player.telegram.chat_id, text=message3, parse_mode="Markdown"))
                        # post(player.telegram.api_url,
                        #      json=dict(chat_id=player.telegram.chat_id, text=message4, parse_mode="Markdown"))
                        new_battle_list.append(newbattleinfo)
                        # player.telegram.send_message('find battle: ' + str(player.all_battles[id]))
                        continue
                if (delta > timedelta(minutes=61)):
                    for i in range(1,5) :
                        bh_watch = str(id) + ":" + str(player.all_battles[id].zone_id) + ":" + str(i)
                        if bh_watch in bh_watch_list:
                            continue
                        place = player.get_my_status(id, div=i)
                        if place > 1:
                            print(bh_watch)
                            if not bh_watch in bh_watch_list:
                                message = 'https://www.erepublik.com/en/military/battlefield/' + str(id) \
                                          + "  check BH in Div: " + str(i)
                                post(player.telegram.api_url, json=dict(chat_id=player.telegram.chat_id, text=message, parse_mode="Markdown"))
                                print(message)
                            bh_watch_list.append(bh_watch)
                        else:
                            print("check BH done: ", "div ", i, place)
                    time.sleep(2)

            print(battles)
            player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))
        except:
            player.report_error("Task error: start_battles")
        ###########################################################
        # over_time
        # player.update_job_info()
        # ot_time = player.my_companies.next_ot_time
        # delta = utils.now() - ot_time
        # print(" next overtime", delta)
        # if delta > timedelta(minutes=1):
        #     player.work_ot()
        ################################################
        next_attack_time = utils.good_timedelta(next_attack_time, timedelta(seconds=150))
        print("149", next_attack_time)
        player.stop_threads.wait(utils.get_sleep_seconds(next_attack_time))


def main():
    player = Citizen(email=CONFIG['email'], password=CONFIG['password'], auto_login=True)
    player.config.interactive = CONFIG['interactive']
    player.config.fight = CONFIG['fight']
    player.config.telegram_chat_id = CONFIG['telegram_chat_id']
    player.config.telegram_token = CONFIG['telegram_token']
    player.set_debug(CONFIG.get('debug', False))
    player.login()
    # if CONFIG.get('start_battles'):
    #     name = "{}-start_battles-{}".format(player.name, threading.active_count() - 1)
    #     state_thread = threading.Thread(target=_battle_launcher, args=(player,), name=name)
    #     state_thread.start()
    ####################################################################
    name = "{}-start_battles_moniter-{}".format(player.name, threading.active_count() - 1)
    state_thread = threading.Thread(target=_battle_monitor, args=(player,), name=name)
    state_thread.start()
    ############################################################################
    # name2 = "{}-start_battles_moniter_all-{}".format(player.name, threading.active_count() - 1)
    # state_thread2 = threading.Thread(target=_battle_monitor_all, args=(player,), name=name2)
    # state_thread2.start()
    #######################################################################
    ############################################################################
    # name2 = "{}-start_battles_moniter_air-{}".format(player.name, threading.active_count() - 1)
    # state_thread2 = threading.Thread(target=_battle_monitor_air, args=(player,), name=name2)
    # state_thread2.start()
    #######################################################################
    ###########################################################
    ################################################


if __name__ == "__main__":
    main()
