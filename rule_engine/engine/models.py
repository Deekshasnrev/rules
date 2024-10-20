from django.db import models

# Create your models here.

class ASTNode(models.Model):
    NODE_TYPES = [
        ('operator', 'Operator'),
        ('operand', 'Operand'),
    ]
    
    node_type = models.CharField(max_length=10, choices=NODE_TYPES)
    value = models.CharField(max_length=255, null=True, blank=True)
    left_child = models.ForeignKey('self', related_name='left', on_delete=models.SET_NULL, null=True, blank=True)
    right_child = models.ForeignKey('self', related_name='right', on_delete=models.SET_NULL, null=True, blank=True)
    is_root = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.node_type}: {self.value}'