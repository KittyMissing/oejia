# coding=utf-8
import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.task_queue.api import AsyncDB
except:
    _logger.info('>>> task_queue is not available, switch to sync model')

    class AsyncDB(object):
        def __init__(self, *args, **kwargs):
                pass
        def __call__(self, f, *args, **kwargs):
            return f
