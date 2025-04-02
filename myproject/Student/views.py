from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Student.models import Studentdetails, Studentmarks
from Student.serializers import StudentDetailSerializer, StudentmarksSerializer

#filter and excel file download
import io
from openpyxl import Workbook
from django.http import HttpResponse

class StudentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Studentdetails.objects.all()
        serializer = StudentDetailSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StudentDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

class StudentuniqueView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            student = Studentdetails.objects.get(pk=pk)
        except Studentdetails.DoesNotExist:
            return Response({'Error': 'Student not found'})
        serializer = StudentDetailSerializer(student)
        return Response(serializer.data)

    def put(self, request, pk):
        student = Studentdetails.objects.get(pk=pk)
        serializer = StudentDetailSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def delete(self, request, pk):
        student = Studentdetails.objects.get(pk=pk)
        student.delete()
        return Response({"message": "Student deleted successfully"})

class StudentmarksView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            student_marks = Studentmarks.objects.get(id=id)
        except Studentmarks.DoesNotExist:
            return Response({'error': 'Student marks not found'})
        
        serializer = StudentmarksSerializer(student_marks)
        return Response(serializer.data)
    
    def put(self, request, id):
        try:
            student_marks = Studentmarks.objects.get(id=id)
        except Studentmarks.DoesNotExist:
            return Response({'error': 'Student marks not found'})
        serializer = StudentmarksSerializer(student_marks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error)
def post(self, request):
        # Check if student exists first
        student_id = request.data.get('student_id')  # assuming you send student_id in the data
        try:
            student = Studentdetails.objects.get(id=student_id)
        except Studentdetails.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

        # If the student exists, check if we need to create or update marks
        marks_data = request.data.get('marks')
        
        try:
            student_marks = Studentmarks.objects.get(student=student)
            # If marks exist, update them
            serializer = StudentmarksSerializer(student_marks, data=marks_data)
        except Studentmarks.DoesNotExist:
            # If no marks record exists for the student, create one
            marks_data['student'] = student  # Link the student
            serializer = StudentmarksSerializer(data=marks_data)

        if serializer.is_valid():
            serializer.save()  # This will either create or update the marks
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ExportExcelView(APIView):
    permission_classes = [IsAuthenticated]
    def  get(self, request):
        students = Studentmarks.objects.filter(
            subject1__gt=50 #use foreign key to check greater than 50
        ) | Studentmarks.objects.filter(
            subject2__gt=50
        ) | Studentmarks.objects.filter(
            subject3__gt=50
        ) | Studentmarks.objects.filter(
            subject4__gt=50
        ) | Studentmarks.objects.filter(
            subject5__gt=50
        ) 
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Student details-excel"
        #headers
        headers = ["ID", "Name", "Email", "Mobile", "Blood Group", "Department","Subject 1", "Subject 2", "Subject 3", "Subject 4", "Subject 5"]
        ws.append(headers)
        #Add filtered data to the sheet
        for student_marks in students:
            std = student_marks.student
            std_data = [
                std.id,
                std.name,
                std.email,
                std.mobile,
                std.blood_group,
                std.department,
                student_marks.subject1,
                student_marks.subject2,
                student_marks.subject3,
                student_marks.subject4,
                student_marks.subject5
            ]
            ws.append(std_data)
        
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=students_filtered.xlsx' 
        
        wb.save(response)
        return response