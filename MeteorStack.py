#!/usr/bin/env python

import wx
import sys
import cv2
import FocusStack


class MeteorStackFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MeteorStackFrame, self).__init__(*args, **kw)

        self.InitUI()

        self.picturesPath = []


    def InitUI(self):

        filemenu= wx.Menu()
        filemenu.Append(100, "Import pictures"," Import pictures")
        filemenu.Append(101, "Save results"," Save results")
        filemenu.Append(102, "E&xit"," Terminate the program")
        editmenu = wx.Menu()
        editmenu.Append(103, "Align + Stack pictures")
        """
        editmenu.Append(104, "Align pictures")
        editmenu.Append(105, "Stack pictures")
        """

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.ImportPictures, id=100)
        self.Bind(wx.EVT_MENU, self.SaveResults, id=101)
        self.Bind(wx.EVT_MENU, self.OnExit, id=102)

        self.Bind(wx.EVT_MENU, self.AlignStack, id=103)
        """
        self.Bind(wx.EVT_MENU, self.Align, id=104)
        self.Bind(wx.EVT_MENU, self.Stack, id=105)
        """
    def ImportPictures(self, event):
        print("import pictures")
        with wx.FileDialog(self, "Import pictures", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            self.picturesPath = fileDialog.GetPaths()


    def SaveResults(self, event):
        print("save results")

    def OnExit(self, event):
        self.Close(True)

    def AlignStack(self, event):
        print("align stack")
        if self.picturesPath == []:
            return #no picture to stack

        print(self.picturesPath)

        focusimages = []
        for img in self.picturesPath:
            print("Reading in file {}".format(img))
            focusimages.append(cv2.imread(format(img)))

        merged = FocusStack.focus_stack(focusimages)
        cv2.imwrite("merged.png", merged)

    """
    def Align(self, event):
        print("align")

    def Stack(self, event):
        print("stack")
    """





if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MeteorStackFrame(None, title='MeteorStack')
    frm.Show()
    app.MainLoop()
