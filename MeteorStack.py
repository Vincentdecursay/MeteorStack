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
        self.focusimages = [] #loaded pictures
        self.stackedimages = []


    def InitUI(self):

        filemenu= wx.Menu()
        filemenu.Append(100, "Import pictures"," Import pictures")
        filemenu.Append(101, "Save results"," Save results")
        filemenu.Append(102, "E&xit"," Terminate the program")
        editmenu = wx.Menu()
        editmenu.Append(103, "Align + Stack pictures")
        editmenu.Append(104, "Align pictures")
        editmenu.Append(105, "Stack pictures")


        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.ImportPictures, id=100)
        self.Bind(wx.EVT_MENU, self.SaveResults, id=101)
        self.Bind(wx.EVT_MENU, self.OnExit, id=102)

        self.Bind(wx.EVT_MENU, self.AlignStack, id=103)
        self.Bind(wx.EVT_MENU, self.Align, id=104)
        self.Bind(wx.EVT_MENU, self.Stack, id=105)


    def ImportPictures(self, event):
        print("import pictures")
        with wx.FileDialog(self, "Import pictures", wildcard="All files (*.*)|*.*",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            self.picturesPath = fileDialog.GetPaths()

            #load pictures
            self.focusimages = []
            for img in self.picturesPath:
                print("Reading in file {}".format(img))
                self.focusimages.append(cv2.imread(format(img)))

            # reset aligned images
            self.align_images = []


    def SaveResults(self, event):

        wildcard = "PNG (*.png)|*.png|" \
                    "Jpeg (*.jpg;*.jpeg)|*.jpg;*.jpeg|" \
                    "Tiff (*.tiff)|*.tiff|"\
                    "All files (*.*)|*.*"

        with wx.FileDialog(self, "Save results","test.png", wildcard=wildcard,
                           style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # save the current contents in the file
            pathname = fileDialog.GetPath()
            cv2.imwrite(pathname, self.stackedimages)

    def OnExit(self, event):
        self.Close(True)

    def AlignStack(self, event):
        print("align stack")
        self.Align(True)
        self.Stack(True)

    def Align(self, event):
        print("align")

        if self.focusimages == []:
            return #no picture to stack

        wait = wx.BusyInfo("Please wait, working...")
        self.align_images = FocusStack.align_images(self.focusimages, cv2.MOTION_HOMOGRAPHY)

    def Stack(self, event):
        print("stack")

        if self.align_images == []:
            if self.focusimages == []:
                return #no images to stack
            else:
                wait = wx.BusyInfo("Please wait, working...")
                merged = FocusStack.focus_stack(self.focusimages)
        else:
            wait = wx.BusyInfo("Please wait, working...")
            merged = FocusStack.focus_stack(self.align_images)

        self.stackedimages = merged



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MeteorStackFrame(None, title='MeteorStack')
    frm.Show()
    app.MainLoop()
