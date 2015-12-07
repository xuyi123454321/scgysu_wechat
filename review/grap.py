from django_cron import CronJobBase, Schedule

class GrapMaterial(CronJobBase):
    '''
    This class is used to grap materials from wechat everyday
    '''

    time_wait = 60*24 # minutes, one day

    schedule = Schedule(run_every_mins = time_wait)
    code = 'scgysu_wechat.review.grap.GrapMaterial'

    def do(self):

