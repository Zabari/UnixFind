#!/usr/bin/env python
###This program was written by Daniel Zabari, and can be used freely as long as this comment is kept
import os, wx, re, itertools

class ExampleFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent)
        self.L=[]
        self.dirL=[]
        self.panel = wx.Panel(self)
        self.searchname = wx.StaticText(self.panel, label="Your Search Query:")
        self.search = wx.TextCtrl(self.panel, size=(140, -1))
        #self.result.SetForegroundColour(wx.RED)
        os.system("cd ..;pwd >> dir.txt")
        os.system("pwd >> ../dir.txt")
        os.system("ls -p | grep \"/\" >> ../dir.txt")
        f=open('../dir.txt','r')
        self.dirL=f.readlines()
        f.close()
        os.system('rm ../dir.txt')
        self.dirL=[line[:-1] for line in self.dirL]
        self.select=wx.Choice(self.panel, choices=['or','and'])
        self.dir=wx.Choice(self.panel, pos=(1,1), choices=self.dirL)
        self.button = wx.Button(self.panel, label="Search")
        # Set sizer for the frame, so we can change frame size to match widgets
        self.windowSizer = wx.BoxSizer()
        self.windowSizer.Add(self.panel, 1, wx.ALL | wx.EXPAND)
        self.results=wx.Choice(self.panel)

        self.open=wx.Button(self.panel, label='Open')
        self.open.Disable()



        # Set sizer for the panel content
        self.sizer = wx.GridBagSizer(10, 10)
        self.sizer.Add(self.dir, (0,0))
        self.sizer.Add(self.searchname, (1, 0))
        self.sizer.Add(self.search, (1, 1))
        self.sizer.Add(self.results,(2,0))
        self.sizer.Add(self.select,(2,1))
        self.sizer.Add(self.open,(3,1))
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
    def lookup(self,L,dirx):
        c=self.select.GetCurrentSelection()
        #print c
        if c==0:#radio whatever = or
            for x in L:
                os.system('find '+dirx+' -iname \'*'+x+'*\' >> results.txt')
        if c==1:#radio whatever = and
            for lL in itertools.permutations(L):
                s="*".join(lL)
                os.system('find '+dirx+' -iname \'*'+s+'*\' >> results.txt')
        f=open('results.txt','r')
        temp=f.readlines()
        f.close()
        os.system('rm results.txt')
        ret=[]
        for x in temp:
            if x not in ret:
                ret.append(x)
        return ret
    def sesame(self,e):
        i=self.results.GetCurrentSelection()
        os.system('nautilus ' + self.L[i])

    def OnButton(self, e):
        self.open.Enable()
        s=self.search.GetValue()
        L=self.lookup(s.split(' '),self.dirL[self.dir.GetCurrentSelection()])
        L=[line[:-1] for line in L]
        self.L=L
        self.results.Clear()
        self.results.AppendItems(L)
        #self.results=wx.Choice(self.panel, choices=L)
        #self.sizer.Add(self.results,(2,0))
        #self.open=wx.Button(self.panel, label='Open')
        #self.sizer.Add(self.open,(3,1))

        #self.panel.SetSizerAndFit(self.border)
        #self.SetSizerAndFit(self.windowSizer)
        self.open.Bind(wx.EVT_BUTTON, self.sesame)

        #os.system("printf '%s' "+new)
        #os.system("echo "+conf)

app = wx.App(False)
frame = ExampleFrame(None)
frame.Show()
app.MainLoop()
