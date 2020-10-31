import classroom
import drive
import npyscreen

Classroom = classroom.Classroom()
ClassroomStuff = classroom.GetClassroomStuff(classroom=Classroom)
Drive = drive.GDrive()

class MyTestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", MainForm())

class MainForm(npyscreen.FormWithMenus, npyscreen.ActionForm):
    def create(self):
        npyscreen.notify("Logging in ..", title='Loading', wide=True)
        Classroom.initialize()
        F = npyscreen.Form(name = "Welcome to Better Classroom",)

        self.m1 = self.add_menu(name="Main Menu")

        courses = getCourseList(ClassroomStuff)

        t3 = F.add(npyscreen.BoxTitle, name="Select course:",
                   scroll_exit = True,
                   contained_widget_arguments={
                       'color': "WARNING", 
                       'widgets_inherit_color': True,}
                   )
        t3.values = [course['name'] for course in courses]
        F.edit()

        F._clear_all_widgets()

        # npyscreen.notify("Getting Materials..", title='Loading', wide=True)

        posts = []
        id = courses[t3.value]['id']
        courseMaterials = ClassroomStuff.getPosts(courseId=id)
        for material in courseMaterials:
            posts.append(material)

        m = F.add(npyscreen.BoxTitle, name="Select Material:",
                   scroll_exit = True,
                   contained_widget_arguments={
                       'color': "WARNING", 
                       'widgets_inherit_color': True}
                   )
        m.values = [post['title'] for post in posts]

        F.edit()

        file_id = posts[m.value]['id']
        title = posts[m.value]['title']
        x = Drive.downloadFile(fileId=file_id, fileName=title)


        F._clear_all_widgets()
        npyscreen.notify("Downloading the file", title='Downloading', wide=True)
        x[0].GetContentFile(x[1])
        F._clear_all_widgets()

        npyscreen.notify("Finished Downloading", title='Success', wide=True)
        

def getCourseList(ClassroomStuff):
    courses = ClassroomStuff.getCourses()
    return courses

if __name__ == "__main__":
    TA = MyTestApp()
    TA.run()
