# from rest_framework import serializers
# from Portfolio.models import PortfolioModel
#
#
# class PortfolioSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PortfolioModel
#         fields = [
#             'bio',
#             'location',
#             'website',
#             'birth_date',
#             'linkedin_url',
#             'github_url',
#             'kaggle_url',
#             'google_scholar_url',
#         ]
#
#     def create(self, validated_data):
#         portfolio_object = PortfolioModel.objects.create(**validated_data)
#         return portfolio_object

from rest_framework import serializers
from .models import (
    Portfolio, WorkExperience, EducationDetail, Project, Publication, Course,
    Skill, Award, PersonalDetail, Language, Startup
)


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = '__all__'
        extra_kwargs = {'title': {'required': False}}

    def create(self, validated_data):
        print(validated_data)
        return WorkExperience.objects.create(**validated_data)


class EducationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationDetail
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tech_used = SkillSerializer(many=True)

    class Meta:
        model = Project
        fields = '__all__'

    def create(self, validated_data):
        skills = validated_data.pop('tech_used', [])

        project = Project.objects.create(**validated_data)

        all_skills = []
        for skill in skills:
            obj = Skill.objects.filter(**skill)
            if not obj.exists():
                obj = Skill.objects.create(**skill)
                all_skills.append(obj)
            else:
                all_skills.append(*obj)
        project.tech_used.set(all_skills)

        return project


class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'


class PersonalDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDetail
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
        extra_kwargs = {'language_name': {'required': False}}


class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = '__all__'
        extra_kwargs = {'name': {'required': False}}


class PortfolioSerializer(serializers.ModelSerializer):
    work_experiences = WorkExperienceSerializer(many=True, required=False)
    education_details = EducationDetailSerializer(many=True, required=False)
    projects = ProjectSerializer(many=True, required=False)
    publications = PublicationSerializer(many=True, required=False)
    courses = CourseSerializer(many=True, required=False)
    skills = SkillSerializer(many=True, required=False)
    awards = AwardSerializer(many=True, required=False)
    personal_details = PersonalDetailSerializer(required=False)
    languages = LanguageSerializer(many=True, required=False)
    startups = StartupSerializer(many=True, required=False)

    class Meta:
        model = Portfolio
        fields = '__all__'

    def create(self, validated_data):
        # Extract related model data
        work_experience_data = validated_data.pop('work_experiences', [])
        education_data = validated_data.pop('education_details', [])
        projects_data = validated_data.pop('projects', [])
        publications_data = validated_data.pop('publications', [])
        courses_data = validated_data.pop('courses', [])
        skills_data = validated_data.pop('skills', [])
        awards_data = validated_data.pop('awards', [])
        personal_details_data = validated_data.pop('personal_details', None)
        languages_data = validated_data.pop('languages', [])
        startup_data = validated_data.pop('startups', [])

        portfolio = Portfolio.objects.create(**validated_data)

        works = []
        for work in work_experience_data:
            obj = WorkExperience.objects.filter(**work)
            if not obj.exists():
                obj = WorkExperience.objects.create(**work)
                works.append(obj)
            else:
                works.append(*obj)
        portfolio.work_experiences.set(works)

        edu = []
        for education in education_data:
            obj = EducationDetail.objects.filter(**education)
            if not obj.exists():
                obj = EducationDetail.objects.create(**education)
                edu.append(obj)
            else:
                edu.append(*obj)
        portfolio.education_details.set(edu)

        proj = []
        for project in projects_data:
            tech = project.pop('tech_used', [])
            obj = Project.objects.filter(**project)
            if not obj.exists():
                project['tech_used'] = tech
                project_s = ProjectSerializer()
                obj = project_s.create(project)
                proj.append(obj)
            else:
                proj.append(*obj)
        portfolio.projects.set(proj)

        pubs = []
        for publication in publications_data:
            obj = Publication.objects.filter(**publication)
            if not obj.exists():
                obj = Publication.objects.create(**publication)
                pubs.append(obj)
            else:
                pubs.append(*obj)
        portfolio.publications.set(pubs)

        courses = []
        for course in courses_data:
            obj = Course.objects.filter(**course)
            if not obj.exists():
                Course.objects.create(**course)
                courses.append(obj)
            else:
                courses.append(*obj)
        portfolio.courses.set(courses)

        skills = []
        for skill in skills_data:
            obj = Skill.objects.filter(**skill)
            if not obj.exists():
                obj = Skill.objects.create(**skill)
                skills.append(obj)
            else:
                skills.append(*obj)
        portfolio.skills.set(skills)

        awards = []
        for award in awards_data:
            obj = Award.objects.filter(**award)
            if not obj.exists():
                obj = Award.objects.create(**award)
            awards.append(obj)
        portfolio.awards.set(awards)

        if personal_details_data:
            deets = PersonalDetail.objects.create(**personal_details_data)
            portfolio.personal_details = deets

        ls = []
        for language in languages_data:
            obj = Language.objects.filter(**language)
            if not obj.exists():
                obj = Language.objects.create(**language)
                ls.append(obj)
            else:
                ls.append(*obj)
        portfolio.languages.set(ls)

        startups = []
        for startup in startup_data:
            obj = Startup.objects.filter(**startup)
            if not obj.exists():
                obj = Startup.objects.create(**startup)
                startups.append(obj)
            else:
                startups.append(*obj)
        portfolio.startups.set(startups)

        return portfolio

