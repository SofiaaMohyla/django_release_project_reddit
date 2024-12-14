from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.

class Rating(models.Model):
    sum_rating = models.IntegerField(default=0)

    def get_rating(self):
        return sum([grade.value for grade in self.grades.all()])

class Grade(models.Model):
    rating = models.ForeignKey(to=Rating, on_delete=models.CASCADE, related_name='grades')
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, related_name='grades')
    value = models.IntegerField(choices=[(1, 'Like'), (-1, 'Dislike')])
    time_create = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rating', 'user')
        ordering = ('-time_create',)
        indexes = [models.Index(fields=['-time_create', 'value'])]
        verbose_name = 'Grade'
        verbose_name_plural = 'Grades'
    
    def __str__(self):
        return f'{self.user.username} {self.value}'

class Branch(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def get_absolute_url(self):
        return reverse('branch-detail', kwargs={'pk': self.pk})

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(auto_now=True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='post', blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.rating:
            self.rating.delete()
        super(Post, self).delete(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk,
                                              'bk': self.branch.pk})

    def __str__(self) -> str:
        return f'{self.title}'

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

class Commentary(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    commentary = models.ForeignKey('Commentary', on_delete=models.CASCADE, related_name='comments', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(auto_now=True)
    rating = models.OneToOneField(Rating, on_delete=models.CASCADE, related_name='comment', blank=True, null=True)

    def delete(self, *args, **kwargs):
        if self.rating:
            self.rating.delete()
        super(Commentary, self).delete(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.text}'
    
    class Meta:
        ordering=['-created']
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
