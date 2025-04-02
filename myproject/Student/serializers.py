from rest_framework import serializers
from Student.models import Studentdetails, Studentmarks

class StudentmarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studentmarks
        fields = ['subject1', 'subject2', 'subject3', 'subject4', 'subject5']
    def update(self, instance, validated_data):
        # Update the test marks if provided
        instance.subject1 = validated_data.get('subject1', instance.subject1)
        instance.subject2 = validated_data.get('subject2', instance.subject2)
        instance.subject3 = validated_data.get('subject3', instance.subject3)
        instance.subject4 = validated_data.get('subject4', instance.subject4)
        instance.subject5 = validated_data.get('subject5', instance.subject5)
        instance.save()
        return instance
    
    def create(self, validated_data):
        # Create a new student marks record if it doesn't exist
        student = validated_data.pop('student')
        student_marks = Studentmarks.objects.create(student=student, **validated_data)
        return student_marks

class StudentDetailSerializer(serializers.ModelSerializer):
    testmarks = StudentmarksSerializer()

    class Meta:
        model = Studentdetails
        fields = '__all__'

    def create(self, validated_data):
        # Extract the testmarks data from validated data
        marks_data = validated_data.pop('testmarks', None)
        
        # Create the student instance
        student = Studentdetails.objects.create(**validated_data)

        # If marks data exists, check if marks already exist for the student
        if marks_data:
            # Try to get an existing Studentmarks instance or create a new one
            student_marks, created = Studentmarks.objects.update_or_create(
                student=student,  # Related to the student
                defaults=marks_data  # If marks already exist, update them
            )

        return student

    def update(self, instance, validated_data):
        # Extract the testmarks data
        marks_data = validated_data.pop('testmarks', None)

        # Update the basic student fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # If marks data exists, check if marks already exist for this student
        if marks_data:
            # Try to get or create the marks for this student
            student_marks, created = Studentmarks.objects.update_or_create(
                student=instance,
                defaults=marks_data  # Update or create based on marks_data
            )

        return instance

