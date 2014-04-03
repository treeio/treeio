# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Cron commands
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.cache import cache
from core.domains import setup_domain
from optparse import make_option
import multiprocessing
import logging
import logging.handlers
import signal
import time
import sys

LOG_LEVELS = {'debug': logging.DEBUG,
              'info': logging.INFO,
              'warning': logging.WARNING,
              'error': logging.ERROR,
              'critical': logging.CRITICAL}

cronlogger = logging.getLogger('CronLogger')
cronlogger.setLevel(logging.DEBUG)


class CronJob(multiprocessing.Process):

    "Single Cron job"

    job = None
    database = 'default'
    priority = 5

    def __init__(self, job, database='default', priority=5, *args, **kwargs):
        super(CronJob, self).__init__(*args, **kwargs)
        self.job = job
        self.priority = priority
        self.database = database
        self._stopped = False

    def sigterm(self, *args, **kwargs):
        cronlogger = logging.getLogger('CronLogger')
        if self._stopped:
            cronlogger.critical('JOB - Terminated ' + unicode(self))
            sys.exit(1)
        else:
            self._stopped = True
            cronlogger.warning('JOB - Early shutdown ' + unicode(self))
            raise KeyboardInterrupt()

    def run(self):
        signal.signal(signal.SIGTERM, self.sigterm)
        setup_domain(self.database)
        cronlogger = logging.getLogger('CronLogger')
        cronlogger.debug('JOB - Starting ' + unicode(self))
        try:
            self.job()
        except KeyboardInterrupt:
            self._stopped = True
        except SystemExit:
            self._stopped = True
        except:
            import traceback
            from hardtree import core
            from django.core.mail import mail_admins
            exc_type, exc_value, exc_traceback = sys.exc_info()
            subject = "CRON Exception for " + \
                unicode(self) + ": " + unicode(exc_type) + \
                " " + unicode(exc_value)
            body = subject + "\n\n"
            body += unicode(core.__file__) + "\n\n"
            for s in traceback.format_tb(exc_traceback):
                body += s + '\n'
            cronlogger.error(subject + '\n' + body)
            mail_admins(subject, body)
        cronlogger.debug('JOB - Finished ' + unicode(self))

    def __repr__(self):
        return 'CronJob ' + unicode(self.database) + ': ' + unicode(self.job)

    def __unicode__(self):
        return self.__repr__()


class CronRunner():

    "Cron runner"

    pool = []
    queue = []
    jobs = []
    sleeptime = 60
    cycle = 1
    _stopped = False

    def __init__(self, databases=[], noloop=False, *args, **kwargs):
        "Capture all cron jobs"

        signal.signal(signal.SIGTERM, self.stop)

        self.databases = databases or []
        self.jobs = []
        self.sleeptime = getattr(settings, 'HARDTREE_CRON_PERIOD', 60)
        self.priority_high = getattr(
            settings, 'HARDTREE_CRON_HIGH_PRIORITY', 10)
        self.priority_low = getattr(settings, 'HARDTREE_CRON_LOW_PRIORITY', 3)
        self.qualify_high = getattr(settings, 'HARDTREE_CRON_QUALIFY_HIGH', 10)
        self.qualify_run = getattr(
            settings, 'HARDTREE_CRON_QUALIFY_RUN', 86400)
        self.poolsize = getattr(settings, 'HARDTREE_CRON_POOL_SIZE', 10)
        self.softkill = getattr(settings, 'HARDTREE_CRON_SOFT_KILL', 0)
        self.hardkill = getattr(settings, 'HARDTREE_CRON_HARD_KILL', -1)
        self.gracewait = getattr(settings, 'HARDTREE_CRON_GRACE_WAIT', 5)
        self.noloop = noloop

        for module in settings.INSTALLED_APPS:
            import_name = str(
                module) + "." + settings.HARDTREE_MODULE_IDENTIFIER
            try:
                hmodule = __import__(import_name, fromlist=[str(module)])
                self.jobs.extend(hmodule.CRON)
            except ImportError:
                pass
            except AttributeError:
                pass

        if not self.databases:
            self.databases = [db for db in settings.DATABASES]

        cronlogger.info('Starting cron...')
        cronlogger.debug('DATABASES: ' + unicode(self.databases))
        cronlogger.debug('CRON_PERIOD: ' + unicode(self.sleeptime))
        cronlogger.debug('CRON_HIGH_PRIORITY: ' + unicode(self.priority_high))
        cronlogger.debug('CRON_LOW_PRIORITY: ' + unicode(self.priority_low))
        cronlogger.debug('CRON_QUALIFY_HIGH: ' + unicode(self.qualify_high))
        cronlogger.debug('CRON_POOL_SIZE: ' + unicode(self.poolsize))
        cronlogger.debug('CRON_SOFT_KILL: ' + unicode(self.softkill))
        cronlogger.debug('CRON_HARD_KILL: ' + unicode(self.hardkill))
        cronlogger.debug('CRON_GRACE_WAIT: ' + unicode(self.gracewait))
        cronlogger.debug('CRON_NO_LOOP: ' + unicode(self.noloop))

    def add_jobs(self):
        "Adds all jobs to the queue"
        cronlogger.info(
            'Adding ' + unicode(len(self.jobs)) + ' jobs to the queue.')
        for db in self.databases:
            cronlogger.debug('ADDING JOBS FOR ' + unicode(db))
            cache_key = 'hardtree_' + db + '_last'
            last_accessed = cache.get(cache_key)
            if last_accessed:
                if last_accessed >= time.time() - int(self.qualify_run):
                    for job in self.jobs:
                        cron = CronJob(job, db, self.priority_low)
                        self.queue.append(cron)
                        cronlogger.debug('JOB ADDED ' + unicode(cron))
                else:
                    cronlogger.debug(
                        'JOB DOES NOT QUALIFY ' + unicode(db) + ': NOT USED in last ' + unicode(self.qualify_run))
            else:
                cronlogger.debug(
                    'JOB DOES NOT QUALIFY ' + unicode(db) + ': NO KEY IN cache')
        cronlogger.debug('Queue: ' + unicode(self.jobs))

    def start(self):
        "Start cron runner"
        self.add_jobs()
        try:
            while not self._stopped:
                if len(self.pool) < self.poolsize:
                    while len(self.queue) > 0 and len(self.pool) < self.poolsize:
                        cron = self.queue.pop()
                        self.pool.append(cron)
                        if cache.has_key('hardtree_%s_last' % (cron.database)):
                            last_accessed = cache.get(
                                'hardtree_%s_last' % (cron.database))
                            if last_accessed > (time.time() - int(self.qualify_high)):
                                cron.priority = self.priority_high
                                cronlogger.debug(
                                    'HIGH PRIORITY set to ' + unicode(cron))
                        cron.start()
                if len(self.queue) == 0:
                    cronlogger.info(
                        'Cron cycle ' + unicode(self.cycle) + ' completed.')
                    self.cycle += 1
                    if self.noloop:
                        self._stopped = True
                    else:
                        self.add_jobs()
                        time.sleep(self.sleeptime)
                cronlogger.debug("POOL SIZE: " + unicode(len(self.pool)))
                for cron in self.pool:
                    cronlogger.debug("POOL JOB: " + unicode(cron) + ', PRIORITY ' +
                                     unicode(cron.priority) + ', ACTIVE: ' + unicode(cron.is_alive()))
                    if not cron.is_alive():
                        self.pool.remove(cron)
                        continue
                    if cron.priority == self.softkill:
                        cron.terminate()
                    elif cron.priority <= self.hardkill:
                        cron.terminate()
                    cron.priority -= 1
                time.sleep(self.sleeptime)
        except KeyboardInterrupt:
            self.stop()

    def stop(self, *args, **kwargs):
        cronlogger.info('Stopping...')
        self._stopped = True
        for cron in self.pool:
            while cron.is_alive():
                cron.terminate()
                time.sleep(self.gracewait)
        cronlogger.debug('Stopped.')
        sys.exit(0)


class Command(BaseCommand):
    args = '[database database ...]'
    help = 'Starts cron runner'
    option_list = BaseCommand.option_list + (
        make_option('-l', '--logfile',
                    action='store',
                    dest='logfile',
                    default='/tmp/hardtree-cron.log',
                    help='Cron log file'
                    ),
        make_option('-d', '--loglevel',
                    type='choice',
                    action='store',
                    dest='loglevel',
                    default='info',
                    choices=[i for i in LOG_LEVELS],
                    help='Logging level'
                    ),
        make_option('-n', '--noloop',
                    action='store_true',
                    dest='noloop',
                    default=False,
                    help='Exit after all jobs are finished'
                    )

    )

    def handle(self, *args, **options):
        loghandler = logging.handlers.RotatingFileHandler(
            options.get('logfile'), maxBytes=100 * 1024 * 1024, backupCount=5)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        loghandler.setFormatter(formatter)
        loghandler.setLevel(LOG_LEVELS[options.get('loglevel')])
        cronlogger.setLevel(LOG_LEVELS[options.get('loglevel')])
        cronlogger.addHandler(loghandler)
        self.runner = CronRunner(args, noloop=options.get('noloop'))
        self.runner.start()
