# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MainWindow ( wx.Frame ):

	def __init__( self):
		wx.Frame.__init__ ( self, None, id = wx.ID_ANY, title = u"Neuroscience Graph Maker", pos = wx.DefaultPosition, size = wx.Size( 1200,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.MenuBar = wx.MenuBar( 0 )
		self.MenuBar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.MenuBar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		self.File = wx.Menu()
		self.New = wx.MenuItem( self.File, wx.ID_ANY, u"New", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.New )

		self.Open = wx.MenuItem( self.File, wx.ID_ANY, u"Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Open )

		self.Save = wx.MenuItem( self.File, wx.ID_ANY, u"Save as...", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Save )

		self.File.AppendSeparator()

		self.Settings = wx.MenuItem( self.File, wx.ID_ANY, u"Settings", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Settings )

		self.File.AppendSeparator()

		self.Export = wx.MenuItem( self.File, wx.ID_ANY, u"Export as...", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Export )

		self.File.AppendSeparator()

		self.Print = wx.MenuItem( self.File, wx.ID_ANY, u"Print", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Print )

		self.File.AppendSeparator()

		self.Exit = wx.MenuItem( self.File, wx.ID_ANY, u"Exit", wx.EmptyString, wx.ITEM_NORMAL )
		self.File.AppendItem( self.Exit )

		self.MenuBar.Append( self.File, u"File" )

		self.SetMenuBar( self.MenuBar )


		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


class MyApp(wx.App):
	def OnInit(self):
		main = MainWindow()
		main.Show()
		return True

app = MyApp(0)
app.MainLoop()