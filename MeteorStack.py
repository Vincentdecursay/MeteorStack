#!/usr/bin/env python

import wx
from threading import *
import sys
import cv2
import FocusStack

ID_IMPORT_PICTURES = wx.NewIdRef(count=1)
ID_SAVE_RESULTS = wx.NewIdRef(count=1)
ID_EXIT = wx.NewIdRef(count=1)
ID_START_ALIGN_AND_STACK = wx.NewIdRef(count=1)
ID_STOP_ALIGN_AND_STACK = wx.NewIdRef(count=1)
ID_START_ALIGN = wx.NewIdRef(count=1)
ID_STOP_ALIGN = wx.NewIdRef(count=1)
ID_START_STACK = wx.NewIdRef(count=1)
ID_STOP_STACK = wx.NewIdRef(count=1)

class RedirectText(object):
    def __init__(self,aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self,string):
        self.out.WriteText(string)

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
        filemenu.Append(ID_IMPORT_PICTURES, "Import pictures"," Import pictures")
        filemenu.Append(ID_SAVE_RESULTS, "Save results"," Save results")
        filemenu.Append(ID_EXIT, "E&xit"," Terminate the program")
        editmenu = wx.Menu()
        editmenu.Append(ID_START_ALIGN_AND_STACK, "Align + Stack pictures")
        editmenu.Append(ID_START_ALIGN, "Align pictures")
        editmenu.Append(ID_START_STACK, "Stack pictures")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        menuBar.Append(editmenu, "&Edit")
        self.SetMenuBar(menuBar)

        self.Bind(wx.EVT_MENU, self.ImportPictures, id=ID_IMPORT_PICTURES)
        self.Bind(wx.EVT_MENU, self.SaveResults, id=ID_SAVE_RESULTS)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_EXIT)

        self.Bind(wx.EVT_MENU, self.AlignStack, id=ID_START_ALIGN_AND_STACK)
        self.Bind(wx.EVT_MENU, self.Align, id=ID_START_ALIGN)
        self.Bind(wx.EVT_MENU, self.Stack, id=ID_START_STACK)


        sizer = wx.GridBagSizer(hgap=5, vgap=5)

        self.log = wx.TextCtrl(self, -1, size=(400, -1), style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        redir = RedirectText(self.log)
        sys.stdout = redir

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
            print(type(merged))
        self.stackedimages = merged



if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    app = wx.App()
    frm = MeteorStackFrame(None, title='MeteorStack')
    frm.Show()
    app.MainLoop()
