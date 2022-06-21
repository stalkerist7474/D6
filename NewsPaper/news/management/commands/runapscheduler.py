import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from datetime import datetime, timedelta
from news.models import Post,Subscriber
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
 
 
logger = logging.getLogger(__name__)
 

def my_job():
    last_week = datetime.today() - timedelta(days=7)
    posts = Post.objects.filter(post_date_created__week=last_week.isocalendar()[1])
    subscribers = Subscriber.objects.filter()
    for obj in posts:  
       
        category_post = list(obj.category.all())
        for sub in subscribers:
            if sub.category in category_post:
                html_content = render_to_string('email_template.html', { 'head': instance.head_of_post, 'text':instance.article_text[:50], 'article_id':instance.id})
                msg = EmailMultiAlternatives(
                    subject=f'Здравствуй, {sub.name_sub.username}. Новая статья в твоём любимом разделе!',
                    body=html_content,
                    from_email='TestDjango1@yandex.ru',
                    to=[sub.email,])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

            else:  
                continue


 
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(week="*/1"),  # Тоже самое что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")