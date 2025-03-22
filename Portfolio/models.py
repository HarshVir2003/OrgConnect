from django.db import models
from django.contrib.auth.models import User


class WorkExperience(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    start_time = models.DateField()
    end_time = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255)
    summary = models.TextField(null=True, blank=True)


class EducationDetail(models.Model):
    university = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    grade = models.FloatField()
    certificate_link = models.URLField(null=True, blank=True)


class Skill(models.Model):
    skill_name = models.CharField(max_length=255)


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    tech_used = models.ManyToManyField(Skill, related_name="projects")
    project_link = models.URLField(null=True, blank=True)


class Publication(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    authors = models.TextField()
    conference_or_journal_name = models.CharField(max_length=255)
    paper_type = models.CharField(max_length=50,
                                  choices=[("Patent", "Patent"), ("Research Paper", "Research Paper"), ("Book", "Book"),
                                           ("Book Chapter", "Book Chapter")])


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    course_link = models.URLField()
    course_duration = models.CharField(max_length=255)
    certificate_link = models.URLField(null=True, blank=True)


class Award(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    certificate_link = models.URLField(null=True, blank=True)


class PersonalDetail(models.Model):
    dob = models.DateField()
    gender = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    current_job = models.CharField(max_length=255)
    employment_status = models.BooleanField()


class Language(models.Model):
    language_name = models.CharField(max_length=255)


class Startup(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255)
    founders = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    annual_turnover = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)


class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=2048)
    location = models.CharField(max_length=1024, null=True, blank=True)
    website = models.URLField(max_length=1024, null=True, blank=True)
    birth_date = models.DateField()
    linkedin_url = models.URLField(null=True, blank=True)
    github_url = models.URLField(null=True, blank=True)
    kaggle_url = models.URLField(null=True, blank=True)
    google_scholar_url = models.URLField(null=True, blank=True)

    work_experiences = models.ManyToManyField(WorkExperience, related_name="portfolios", blank=True)
    education_details = models.ManyToManyField(EducationDetail, related_name="portfolios", blank=True)
    projects = models.ManyToManyField(Project, related_name="portfolios", blank=True)
    publications = models.ManyToManyField(Publication, related_name="portfolios", blank=True)
    courses = models.ManyToManyField(Course, related_name="portfolios", blank=True)
    skills = models.ManyToManyField(Skill, related_name="portfolios", blank=True)
    awards = models.ManyToManyField(Award, related_name="portfolios", blank=True)
    personal_details = models.OneToOneField(PersonalDetail, on_delete=models.CASCADE, null=True, blank=True)
    languages = models.ManyToManyField(Language, related_name="portfolios", blank=True)
    privacy_level = models.IntegerField(choices=[(0, "Personal"), (1, "Contacts"), (2, "Everyone")])
    startups = models.ManyToManyField(Startup, related_name="portfolios", blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Portfolio Model'
        db_table = 'user_portfolio'
