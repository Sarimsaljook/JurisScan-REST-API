import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection

class UploadFileView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        file = request.data.get('file')
        file_path = request.data.get('file_path')
        if not user_id or not file:
            return Response({'error': 'user_id and file are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save file to user's table
        table_name = f'user_{user_id}'
        with connection.cursor() as cursor:
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {table_name} (file_name VARCHAR(255), file_path VARCHAR(255), file LONGBLOB)")
            cursor.execute(f"INSERT INTO {table_name} (file_name, file_path, file) VALUES (%s, %s, %s)",
                           [file.name, file_path, file.read()])

        return Response({'message': 'File uploaded successfully'}, status=status.HTTP_201_CREATED)


class GetUserFilesView(APIView):
    def get(self, request, user_id):
        table_name = f'user_{user_id}'
        with connection.cursor() as cursor:
            cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
            if cursor.fetchone() is None:
                return Response({'error': 'User table does not exist'}, status=status.HTTP_404_NOT_FOUND)

            cursor.execute(f"SELECT file_name, file_path, file FROM {table_name}")
            files = cursor.fetchall()

            response_files = [
                {'file_name': file[0], 'file_path': file[1], 'file_content': base64.b64encode(file[2]).decode('utf-8')}
                for file in files]

            return Response({'files': response_files}, status=status.HTTP_200_OK)
