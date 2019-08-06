from apscheduler.schedulers.blocking import BlockingScheduler
import spider_job.baidu_hot as baidu_hot
import spider_job.sina_hot as sina_hot

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour='0-23')
def baidu_hot_job():
    print('------------ baidu hot job start! -----------')
    baidu_hot.baidu_main_job()
    print('------------ baidu hot job end! --------------')


@scheduler.scheduled_job('cron', hour='0-23')
def sina_hot_job():
    print('------------ sina hot job start! -----------')
    sina_hot.sina_main_job()
    print('------------ sina hot job end! --------------')

scheduler.start()
