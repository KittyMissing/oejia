# coding=utf-8
import logging

from celery import Celery
from kombu import Exchange, Queue
from odoo.tools import config


_logger = logging.getLogger('Celery Worker')

class Task(object):

    def __init__(self):
        pass

class DBQ(object):

    def __init__(self, name='dbq'):
        pass


    def task(self, *opt, **kopt):
        def wrapper(f):
            def _wrapper(*args, **kwargs):
                return f(*args, **kargs)
            return _wrapper
        return wrapper



app = Celery('celery_queue')


class CeleryConfig():
    # 默认的队列
    celery_default_queue = config.get('celery_default_queue', 'odoo10')
    # 定义的所有队列
    celery_queues = config.get('celery_queues', "")

    BROKER_URL = config.get('celery_broker_url')
    CELERY_DEFAULT_QUEUE = celery_default_queue
    CELERY_QUEUES = (
        Queue(celery_default_queue, Exchange(celery_default_queue),
              routing_key=celery_default_queue, durable=True),
    )
    for queue in filter(lambda q: q.strip(), celery_queues.split(",")):
        CELERY_QUEUES = CELERY_QUEUES + \
            (Queue(queue, Exchange(queue), routing_key=queue, durable=True),)

app.config_from_object(CeleryConfig)

if config.get('celery_result_backend_db'):
    app.conf.result_backend = 'odoo.addons.task_queue.backends.ExtDatabaseBackend'#'db+postgresql://user:passwd@localhost/celery_result'
    app.conf.result_backend_db = config.get('celery_result_backend_db')
    app.conf.task_ignore_result = True
    app.conf.task_store_errors_even_if_ignored = True


@app.task
def add(x,y):
    return x+y


import odoo
from odoo.api import Environment
from odoo.modules.registry import Registry

@app.task(name='odoo.addons.celery_queue.tasks.execute')
def execute(conf_attrs, dbname, uid, obj, method, *args, **kwargs):
    _logger.info(str([dbname, uid, obj, method, args, kwargs]))

    if conf_attrs and len(conf_attrs.keys())>1:
        for attr, value in conf_attrs.items():
            odoo.tools.config[attr] = value
    with Environment.manage():
        registry = Registry(dbname)
        cr = registry.cursor()
        context = 'context' in kwargs and kwargs.pop('context') or {}
        env = Environment(cr, uid, context)
        cr.autocommit(True)
        # odoo.api.Environment._local.environments = env
        try:
            Model = env[obj]
            args = list(args)
            _logger.info('>>> %s'%str(args))
            ids = args.pop(0)
            if ids:
                target = Model.search([('id', 'in', ids)])
            else:
                target = Model
            getattr(env.registry[obj], method)(target, *args, **kwargs)
            # Commit only when function finish
            # env.cr.commit()
        except Exception as exc:
            env.cr.rollback()
            import traceback;traceback.print_exc()
            raise exc
            #try:
            #    raise execute.retry(
            #        queue=execute.request.delivery_info['routing_key'],
            #        exc=exc, countdown=(execute.request.retries + 1) * 60,
            #        max_retries=5)
            #except Exception as retry_exc:
            #    raise retry_exc
        finally:
            env.cr.close()
    return True
