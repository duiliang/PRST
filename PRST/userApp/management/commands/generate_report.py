# 在你的应用目录中创建一个名为 management/commands/generate_report.py 的新文件

from django.core.management.base import BaseCommand
from ...report_generations import generate_weekly_report

class Command(BaseCommand):
    help = 'Generate a weekly report'

    def handle(self, *args, **kwargs):
        file_name = generate_weekly_report()
        self.stdout.write(self.style.SUCCESS(f'Successfully generated report: {file_name}'))
