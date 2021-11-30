import win32com.client

app = win32com.client.Dispatch("PowerPoint.Application")
pptfile = app.Presentations.Open(,ReadOnly=0, Untitled=0,
WithWindow=1)#Open the desired ppt file


class ppt:
    def __init__(self):
        self.objCOM = app.Presentations.Open(FileName="path_to_file",    WithWindow=1)
