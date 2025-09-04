from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

class DebateStatus(models.TextChoices):
	PENDING = 'PENDING', '作成直後'
	IN_PROGRESS = 'IN_PROGRESS', '自動進行中'
	COMPLETED_AI = 'COMPLETED_AI', 'AIが完了判断'
	TERMINATED_BY_USER = 'TERMINATED_BY_USER', 'ユーザーが中断'
	FAILED = 'FAILED', 'エラー発生'

class Debate(models.Model):
	topic = models.CharField(max_length=255)
	agents = models.ManyToManyField('agents.Agent', related_name='debates')
	status = models.CharField(
		max_length=32,
		choices=DebateStatus.choices,
		default=DebateStatus.PENDING
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
	debate = models.ForeignKey(Debate, on_delete=models.CASCADE, related_name='messages')
	agent = models.ForeignKey('agents.Agent', on_delete=models.CASCADE)
	content = models.TextField()
	turn = models.PositiveIntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
