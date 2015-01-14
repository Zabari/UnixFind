#!/usr/bin/env python
###This program was written by Daniel Zabari, and can be used freely as long as this comment is kept
import os, wx, re, itertools

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.L=[]
        self.panel = wx.Panel(self)
        self.searchname = wx.StaticText(self.panel, label="Your Search Query:")
        self.search = wx.TextCtrl(self.panel, size=(140, -1))
        #self.result.SetForegroundColour(wx.RED)
        self.select=wx.Choice(self.panel, choices=['or','and'])
        self.button = wx.Button(self.panel, label="Search")
        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)


        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(10, 10)
        self.sizer.Add(self.searchname, (0, 0))
        self.sizer.Add(self.search, (0, 1))
        self.sizer.Add(self.select,(1,1))
        #self.sizer.Add(self.result, (0, 1))
        self.sizer.Add(self.button, (3, 0))


        # Set simple sizer for a nice border
        self.border = wx.BoxSizer()
        self.border.Add(self.sizer, 1, wx.ALL | wx.EXPAND, 5)

        # Use the sizers
        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)

        # Set event handlers
        self.button.Bind(wx.EVT_BUTTON, self.OnButton)
    def lookup(self,L):
        c=self.select.GetCurrentSelection()
        #print c
        if c==0:#radio whatever = or
            for x in L:
                os.system('find . -iname \'*'+x+'*\' >> results.txt')
        if c==1:#radio whatever = and
            for lL in itertools.permutations(L):
                s="*".join(lL)
                os.system('find . -iname \'*'+s+'*\' >> results.txt')
        f=open('results.txt','r')
        ret=f.readlines()
        f.close()
        os.system('rm results.txt')
        for x in ret:
            if ret.count(x)>1:
                ret.remove(x)
        return ret
    def sesame(self,e):
        i=self.results.GetCurrentSelection()
        os.system('nautilus ' + self.L[i])

    def OnButton(self, e):
        self.button.Disable()
        s=self.search.GetValue()
        L=self.lookup(s.split(' '))
        L=[line[:-1] for line in L]
        self.L=L
        self.results=wx.Choice(self.panel, choices=L)
        self.sizer.Add(self.results,(2,0))
        self.open=wx.Button(self.panel, label='Open')
        self.sizer.Add(self.open,(3,1))

        self.panel.SetSizerAndFit(self.border)
        self.SetSizerAndFit(self.windowSizer)
        self.open.Bind(wx.EVT_BUTTON, self.sesame)

        #os.system("printf '%s' "+new)
        #os.system("echo "+conf)

app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()
