# import logging
# from datetime import datetime, timedelta, time, timezone
#
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
#
# from news.models import Post, Category, User
# from django.db.models import Q
#
# from apscheduler.schedulers.blocking import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# from django.conf import settings
# from django.core.management.base import BaseCommand
# from django_apscheduler import util
# from django_apscheduler.jobstores import DjangoJobStore
# from django_apscheduler.models import DjangoJobExecution
#
# logger = logging.getLogger(__name__)
#
#
# def my_job():
#     week_ago = datetime.combine(datetime.today() - timedelta(days=7), time.min).replace(tzinfo=timezone.utc)
#     now = datetime.combine(datetime.today() - timedelta(days=1), time.max).replace(tzinfo=timezone.utc)
#     posts = Post.objects.filter(time_create__gte=week_ago, time_create__lte=now)
#     categories = set(Post.objects.filter(time_create__gte=week_ago, time_create__lte=now).values_list('category__pk', flat=True))
#     subscribers = User.objects.filter(subscription__category__in = categories).distinct().values_list('email', flat=True)
#     print(subscribers)
#     html_context = render_to_string(
#         'weeklyposts.html',
#         {
#             'link':settings.SITE_URL,
#             'posts':posts,
#         }
#     )
#     msg = EmailMultiAlternatives(
#         subject='Статьи за неделю',
#         body='',
#         from_email=settings.EMAIL_HOST_USER,
#         to=subscribers
#     )
#     msg.attach_alternative(html_context, 'text/html')
#     msg.send()
#     pass
#
#
# # The `close_old_connections` decorator ensures that database connections,
# # that have become unusable or are obsolete, are closed before and after your
# # job has run. You should use it to wrap any jobs that you schedule that access
# # the Django database in any way.
# @util.close_old_connections
# def delete_old_job_executions(max_age=604_800):
#     """
#     This job deletes APScheduler job execution entries older than `max_age`
#     from the database.
#     It helps to prevent the database from filling up with old historical
#     records that are no longer useful.
#
#     :param max_age: The maximum length of time to retain historical
#                     job execution records. Defaults to 7 days.
#     """
#     DjangoJobExecution.objects.delete_old_job_executions(max_age)
#
#
# class Command(BaseCommand):
#     help = "Runs APScheduler."
#
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")
#
#         scheduler.add_job(
#             my_job,
#             #trigger=CronTrigger(day_of_week="thu", hour="15", minute="02"),  # Every 10 seconds
#             trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
#             id="my_job",  # The `id` assigned to each job MUST be unique
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added job 'my_job'.")
#
#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(day_of_week="mon", hour="00", minute="00"),
#             id="delete_old_job_executions",
#             max_instances=1,
#             replace_existing=True,
#         )
#         logger.info("Added weekly job: 'delete_old_job_executions'.")
#
#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")successfully