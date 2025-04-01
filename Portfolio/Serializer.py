from rest_framework import serializers
from .models import (
    Portfolio, WorkExperience, EducationDetail, Project, Publication, Course,
    Skill, Award, PersonalDetail, Language, Startup
)


class WorkExperienceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = WorkExperience
        fields = '__all__'


class EducationDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = EducationDetail
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Skill
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    tech_used = SkillSerializer(many=True)
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

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
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Publication
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class AwardSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Award
        fields = '__all__'


class PersonalDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = PersonalDetail
        fields = '__all__'


class LanguageSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Language
        fields = '__all__'


class StartupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    delete = serializers.BooleanField(required=False, default=False, write_only=True)

    class Meta:
        model = Startup
        fields = '__all__'


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
        for data in validated_data:
            d = validated_data.get(data)
            if type(d) is dict:
                d.pop('id', 0)
                d.pop('delete', False)
                validated_data[data] = d
            elif type(d) is list:
                temp = []
                for x in d:
                    x.pop('id', 0)
                    x.pop('delete', False)
                    temp.append(x)
                validated_data[data] = temp

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
                obj = Course.objects.create(**course)
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
            else:
                awards.append(*obj)
        portfolio.awards.set(awards)

        if personal_details_data:
            deets = PersonalDetail.objects.create(**personal_details_data)
            portfolio.personal_details = deets
            portfolio.save()

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

    def update(self, instance, validated_data):
        def segregrate_data(data):
            add = []
            update = []
            delete = []

            print(data)

            for x in data:
                if x:
                    if x.get('delete', False):
                        x.pop('delete')
                        delete.append(x)
                    elif x.get('id', None) is not None:
                        update.append(x)
                    else:
                        add.append(x)

            return [add, update, delete]

        def patch_helper(db, instance_attr, data):
            nonlocal instance
            add, update, delete = segregrate_data(data)
            work_experiences = []
            for work_experience in add:
                obj = db.objects.filter(**work_experience)
                if obj.exists():
                    if not eval(f'instance.{instance_attr}.filter(**work_experience).exists()'):
                        work_experiences.append(*obj)
                else:
                    work_experiences.append(db.objects.create(**work_experience))
            if work_experiences:
                for x in work_experiences:
                    eval(f'instance.{instance_attr}.add(x)')

            work_experiences = []
            for work_experience in update:
                if work_experience.get('id', None) is not None:
                    obj = eval(f"instance.{instance_attr}.filter(id=work_experience.get('id'))")
                    if obj.exists():
                        eval(f"instance.{instance_attr}.remove(*obj)")
                        work_experience.pop('id', 0)
                        work_experiences.append(db.objects.create(**work_experience))
            if work_experiences:
                for x in work_experiences:
                    eval(f"instance.{instance_attr}.add(x)")

            for work_experience in delete:
                obj = eval(f"instance.{instance_attr}.filter(**work_experience)")
                if obj.exists():
                    eval(f"instance.{instance_attr}.remove(*obj)")

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

        patch_helper(WorkExperience, "work_experiences", work_experience_data)
        patch_helper(EducationDetail, 'education_details', education_data)
        patch_helper(Publication, 'publications', publications_data)
        patch_helper(Course, 'courses', courses_data)
        patch_helper(Skill, 'skills', skills_data)
        patch_helper(Award, 'awards', awards_data)
        patch_helper(Language, 'languages', languages_data)
        patch_helper(Startup, 'startups', startup_data)

        add_personal, update_personal, delete_personal = segregrate_data([personal_details_data])

        if add_personal:
            obj = PersonalDetail.objects.create(**add_personal[0])
            instance.personal_details = obj
            instance.save()
        elif update_personal:
            obj = PersonalDetail.objects.filter(id=update_personal[0].get('id'))
            obj.delete()
            instance.personal_details = PersonalDetail.objects.create(**update_personal[0])
            instance.save()
        elif delete_personal:
            instance.personal_details = None
            instance.save()

        add_projects, update_projects, delete_projects = segregrate_data(projects_data)

        projs = []
        if add_projects:
            serial = ProjectSerializer()
            for proj in add_projects:
                projs.append(serial.create(proj))

            for x in projs:
                instance.projects.add(x)

        if delete_projects:
            for proj in delete_projects:
                obj = instance.projects.filter(id=proj.get('id'))
                if obj.exists():
                    instance.projects.remove(*obj)

        return instance
