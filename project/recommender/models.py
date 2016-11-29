from django.db import models

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=60)
    sector = models.IntegerField(default=0)
    mode = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    degree = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    duration = models.FloatField(default=0)
    duration_id = models.IntegerField(default=0)
    sectorStr = models.CharField(max_length=60)
    modeStr = models.CharField(max_length=60)
    levelStr = models.CharField(max_length=60)
    degreeStr = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class User(models.Model):
    #User profile
    #name = models.CharField(max_length=60)
    age = models.IntegerField(default=0)        # Age
    gender = models.IntegerField(default=0)     # Gender
    edu = models.IntegerField(default=0)        # Highest level of education
    emp = models.IntegerField(default=0)        # Employment status
    #User preferences
    mode = models.IntegerField(default=0)
    level = models.IntegerField(default=0)
    degree = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    sector1 = models.IntegerField(default=0)
    sector2 = models.IntegerField(default=0)
    sector3 = models.IntegerField(default=0)
    sector4 = models.IntegerField(default=0)
    sector5 = models.IntegerField(default=0) 


class Rating(models.Model):
    userId = models.IntegerField(default=0)
    courseId = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return 'user'+str(self.userId)+'_'+'course'+str(self.courseId)