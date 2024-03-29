from datetime import timedelta

from erepublik import Citizen, utils

CONFIG = {
    'email': 'player@email.com',
    'password': 'Pa$5w0rd!',
    'interactive': True,
    'debug': True
}


# noinspection DuplicatedCode
def main():
    player = Citizen(email=CONFIG['email'], password=CONFIG['password'], auto_login=False)
    player.config.interactive = CONFIG['interactive']
    player.config.fight = CONFIG['fight']
    player.set_debug(CONFIG.get('debug', False))
    player.login()
    now = player.now.replace(second=0, microsecond=0)
    dt_max = now.replace(year=9999)
    tasks = {
        'eat': now,
    }
    if player.config.work:
        tasks.update({'work': now})
    if player.config.train:
        tasks.update({'train': now})
    if player.config.ot:
        tasks.update({'ot': now})
    if player.config.wam:
        tasks.update({'wam': now.replace(hour=14, minute=0)})
    while True:
        try:
            player.update_all()
            if tasks.get('work', dt_max) <= now:
                player.write_log("Doing task: work")
                player.update_citizen_info()
                player.work()
                if player.config.ot:
                    tasks['ot'] = now
                player.collect_daily_task()
                next_time = utils.good_timedelta(now.replace(hour=0, minute=0, second=0), timedelta(days=1))
                tasks.update({'work': next_time})

            if tasks.get('train', dt_max) <= now:
                player.write_log("Doing task: train")
                player.update_citizen_info()
                player.train()
                player.collect_daily_task()
                next_time = utils.good_timedelta(now.replace(hour=0, minute=0, second=0), timedelta(days=1))
                tasks.update({'train': next_time})

            if tasks.get('wam', dt_max) <= now:
                player.write_log("Doing task: Work as manager")
                success = player.work_as_manager()
                player.eat()
                if success:
                    next_time = utils.good_timedelta(now.replace(hour=14, minute=0, second=0, microsecond=0),
                                                     timedelta(days=1))
                else:
                    next_time = utils.good_timedelta(now.replace(second=0, microsecond=0), timedelta(minutes=30))

                tasks.update({'wam': next_time})

            if tasks.get('eat', dt_max) <= now:
                player.write_log("Doing task: eat")
                player.eat()

                if player.energy.food_fights > player.energy.limit // 10:
                    next_minutes = 12
                else:
                    next_minutes = (player.energy.limit - 5 * player.energy.interval) // player.energy.interval * 6

                next_time = player.energy.reference_time + timedelta(minutes=next_minutes)
                tasks.update({'eat': next_time})

            if tasks.get('ot', dt_max) <= now:
                player.write_log("Doing task: ot")
                if now > player.my_companies.next_ot_time:
                    player.work_ot()
                    next_time = now + timedelta(minutes=60)
                else:
                    next_time = player.my_companies.next_ot_time
                tasks.update({'ot': next_time})

            closest_next_time = dt_max
            next_tasks = []
            for task, next_time in sorted(tasks.items(), key=lambda s: s[1]):
                next_tasks.append("{}: {}".format(next_time.strftime('%F %T'), task))
                if next_time < closest_next_time:
                    closest_next_time = next_time
            sleep_seconds = int(utils.get_sleep_seconds(closest_next_time))
            if sleep_seconds <= 0:
                player.write_log(f"Loop detected! Offending task: '{next_tasks[0]}'")
            player.write_log("My next Tasks and there time:\n" + "\n".join(sorted(next_tasks)))
            player.write_log("Sleeping until (eRep): {} (sleeping for {}s)".format(
                closest_next_time.strftime("%F %T"), sleep_seconds))
            seconds_to_sleep = sleep_seconds if sleep_seconds > 0 else 0
            player.sleep(seconds_to_sleep)
        except Exception as e:
            player.report_error(f"Task main loop ran into error: {e}")


if __name__ == "__main__":
    main()
