from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid
from django.utils import timezone

# Create your models here.

# =======================================================================================
class Poll(models.Model):

    uuid = models.UUIDField(null=False, blank=False, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=100, blank=True, default='')


    # -----------------------------------------------------------------------------------
    def __str__(self):
        return '{}'.format(self.name)

    # -----------------------------------------------------------------------------------
    class Meta:
        db_table = 'poll'
        verbose_name = _('Poll')
        verbose_name_plural = _('Polls')

# =======================================================================================
class PollOption(models.Model):

    poll = models.ForeignKey(Poll, null=False, blank=False,related_name='poll',on_delete=models.DO_NOTHING)
    uuid = models.UUIDField(null=False, blank=False, default=uuid.uuid4, editable=False, db_index=True)
    option_name = models.CharField(max_length=100, blank=True, default='')

    # -----------------------------------------------------------------------------------
    def __str__(self):
        return '{}-{}'.format(self.poll.name,self.option_name)

    # -----------------------------------------------------------------------------------
    class Meta:
        db_table = 'poll_option'
        verbose_name = _('Option')
        verbose_name_plural = _('Options')

# =======================================================================================
class PollVote(models.Model):

    option = models.ForeignKey(PollOption, null=False, blank=False,related_name='option',on_delete=models.DO_NOTHING)
    vote_date = models.DateTimeField(null=False, blank=False, default=timezone.now, editable=False)
    ip = models.CharField(max_length=100, blank=True, default='')

    # -----------------------------------------------------------------------------------
    def __str__(self):
        return '{}'.format(self.option)

    # -----------------------------------------------------------------------------------
    class Meta:
        db_table = 'poll_vote'
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

# =======================================================================================