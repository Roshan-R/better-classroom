from __future__ import print_function
import pickle
import os.path
import io
from apiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
# pylint: disable=import-error
from apiclient.http import BatchHttpRequest

SCOPES = [
    # 'https://www.googleapis.com/auth/classroom.coursework.students.readonly',
    'https://www.googleapis.com/auth/classroom.courses.readonly',
    'https://www.googleapis.com/auth/classroom.rosters',
    'https://www.googleapis.com/auth/classroom.rosters.readonly',
    'https://www.googleapis.com/auth/classroom.profile.emails',
    'https://www.googleapis.com/auth/classroom.profile.photos',
    'https://www.googleapis.com/auth/classroom.coursework.me',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/classroom.courseworkmaterials',
# 'https://www.googleapis.com/auth/classroom.coursework.me.readonly',
'https://www.googleapis.com/auth/classroom.coursework.students'
]

class GetClassroomStuff():
    gclassroom = None

    def __init__(self, classroom):
        self.gclassroom = classroom

    def getCourses(self):
        """ Gets list of course names """

        if 'courses' in globals():
            return

        results = self.gclassroom.service.courses().list(pageSize=100).execute()
        global courses
        courses = results.get('courses', [])

        courseNames = []
        for course in courses:
            courseNames.append(dict({'id': course['id'], 'name': course['name']}))

        return courseNames

    def getPosts(self, courseId):
        """ Gets classroom posts """
        # results = self.gclassroom.service.courses().courseWork().list(courseId=courseId).to_json()
        try:
            # results = self.gclassroom.service.courses().courseWork().list(courseId=courseId).execute()
            results = self.gclassroom.service.courses().courseWorkMaterials().list(courseId=courseId).execute()
            global courses
            # print(str(results))
            materials =  results['courseWorkMaterial']
            materialsList = []
            for material in materials:
                # print(str(material))
                # title = str(material['title'])
                files = material['materials']
                for file in files:
                    title = str(file['driveFile']['driveFile']['title'])
                    fileId = file['driveFile']['driveFile']['id']
                    materialsList.append(dict({'title': title, 'id': fileId}))

        except Exception as e:
            materialsList=[]
            print(str(e))

        # courses = results.get('courseWork', [])
        # print(str(courses))
        # return str(courses)
        return materialsList

    def downloadMaterial(self, fileId, filename):
        file_id = fileId
        request = self.gclassroom.driveService.files().get_media(fileId=file_id)
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        
    
class Classroom:
    service = None
    driveService = None

    def initialize(self):
        creds = None
        drive_creds = None

        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credential.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        # repeating process for drive credentials
        if os.path.exists('drive_token.pickle'):
            with open('drive_token.pickle', 'rb') as token:
                creds = pickle.load(token)

        # If there are no (valid) credentials available, let the user log in.
        if not drive_creds or not drive_creds.valid:
            if drive_creds and drive_creds.expired and drive_creds.refresh_token:
                drive_creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'drive_credential.json', SCOPES)
                drive_creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('drive_token.pickle', 'wb') as token:
                pickle.dump(drive_creds, token)


        self.service = build('classroom', 'v1', credentials=creds)
        self.driveService = build('drive', 'v3', credentials=drive_creds)

