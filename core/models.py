from django.db import models
from django.db.models import F
from django.utils import timezone


class PlatformUser(models.Model):

    bale_user_id = models.BigIntegerField(unique=True)

    username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )

    first_seen = models.DateTimeField(default=timezone.now)

    last_seen = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.bale_user_id)


class BotInteraction(models.Model):

    bot_name = models.CharField(max_length=50)

    user = models.ForeignKey(
        PlatformUser,
        on_delete=models.CASCADE
    )

    command = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bot_name} | {self.user} | {self.command}"


class CommandStat(models.Model):

    bot_name = models.CharField(max_length=50)

    command = models.CharField(max_length=100)

    count = models.IntegerField(default=0)

    class Meta:
        unique_together = ("bot_name", "command")

    def __str__(self):
        return f"{self.bot_name} | {self.command}: {self.count}"

    @classmethod
    def increment(cls, bot_name, command):
        rows = cls.objects.filter(bot_name=bot_name, command=command).update(
            count=F("count") + 1
        )
        if not rows:
            cls.objects.get_or_create(
                bot_name=bot_name, command=command, defaults={"count": 1}
            )
