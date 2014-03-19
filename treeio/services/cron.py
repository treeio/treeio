# encoding: utf-8
# Copyright 2011 Tree.io Limited
# This file is part of Treeio.
# License www.tree.io/license

"""
Services Cron jobs
"""
from treeio.services.models import TicketQueue, TicketRecord
from django.core.urlresolvers import reverse
import datetime


def tickets_escalate():
    "Automatically move tickets to upper queues when no action taken"

    # Collect queues which have waiting time and next queue specified
    queues = TicketQueue.objects.filter(
        waiting_time__isnull=False, next_queue__isnull=False)
    now = datetime.datetime.now()

    for queue in queues:
        if queue.waiting_time and queue.next_queue:
            # Calculate the timeframe outside of which idle tickets should be
            # escalated
            delta = datetime.timedelta(seconds=int(queue.waiting_time))
            timeframe = now - delta

            # Collect tickets ourside the timeframe
            tickets = queue.ticket_set.filter(
                date_created__lt=timeframe, status__active=True)
            for ticket in tickets:
                # Identify if any recent updates have been made on the ticket
                updates = ticket.updates.filter(
                    date_created__gte=timeframe).exists()
                if not updates:
                    ticket.queue = queue.next_queue
                    ticket.auto_notify = False
                    ticket.save()
                    record = TicketRecord(record_type='update')
                    record.format_message = 'Ticket automatically escalated from <a href="' + \
                        reverse('services_queue_view', args=[queue.id]) + \
                        '">' + unicode(queue) + '</a> to <a href="' + \
                        reverse('services_queue_view', args=[queue.next_queue.id]) + \
                        '">' + \
                        unicode(queue.next_queue) + '</a>.'
                    record.author = ticket.creator
                    record.save()
                    record.about.add(ticket)
                    ticket.set_last_updated()
