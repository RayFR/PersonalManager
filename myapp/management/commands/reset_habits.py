from django.core.management.base import BaseCommand
from myapp.models import Habit
from django.utils import timezone

class Command(BaseCommand):
    help = 'Resets the completed status of habits every day'

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        habits_reset = Habit.objects.filter(completed=True).update(completed=False)
        self.stdout.write(f'Successfully reset {habits_reset} habits on {today}.')
