import wx, wx.html
import sys


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Neuroscience Graph Maker", pos=(150,150), size=(1200,700))

        self.InitUI()

    def InitUI(self):
        # Create the status bar
        self.CreateStatusBar()

        self.InitMenuBar()

        # Top level frame stuff
        self.panel = wx.Panel(self)
        self.Centre()

    def InitMenuBar(self):
        # Menu Bar Stuff
        self.MenuBar = wx.MenuBar()

        # File Menu
        self.FileMenu = wx.Menu()

        self.NewItem = wx.MenuItem(self.FileMenu, wx.ID_NEW, help="Create a new project")
        self.FileMenu.AppendItem(self.NewItem)

        self.OpenItem = wx.MenuItem(self.FileMenu, wx.ID_OPEN, help="Open an existing project")
        self.FileMenu.AppendItem(self.OpenItem)

        self.SaveItem = wx.MenuItem(self.FileMenu, wx.ID_SAVE, help="Save the current project")
        self.FileMenu.AppendItem(self.SaveItem)

        self.SaveAsItem = wx.MenuItem(self.FileMenu, wx.ID_SAVEAS, help="Save the current project with a different filename")
        self.FileMenu.AppendItem(self.SaveAsItem)

        self.FileMenu.AppendSeparator()

        self.SettingsItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="Settings", help="Edit Application Settings")
        self.FileMenu.AppendItem(self.SettingsItem)

        self.FileMenu.AppendSeparator()

        self.ImportItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="Import", help="Import MATLAB data")
        self.FileMenu.AppendItem(self.ImportItem)

        self.ExportAsItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="Export as...", help="Open the export dialog to export data")
        self.FileMenu.AppendItem(self.ExportAsItem)

        self.FileMenu.AppendSeparator()

        self.PrintItem = wx.MenuItem(self.FileMenu, wx.ID_PRINT, help="Print the data")
        self.FileMenu.AppendItem(self.PrintItem)

        self.FileMenu.AppendSeparator()

        self.ExitItem = wx.MenuItem(self.FileMenu, wx.ID_EXIT, text="Exit")
        self.FileMenu.AppendItem(self.ExitItem)

        self.MenuBar.Append(self.FileMenu, "File")

        # Edit Menu
        self.EditMenu = wx.Menu()

        self.UndoItem = wx.MenuItem(self.EditMenu, wx.ID_UNDO)
        self.EditMenu.AppendItem(self.UndoItem)

        self.MenuBar.Append(self.EditMenu, "Edit")

        self.SetMenuBar(self.MenuBar)
        self.Bind(wx.EVT_MENU, self.OnQuit, self.ExitItem)

    def OnQuit(self, e):
        self.Close()

class MyApp(wx.App):
    def OnInit(self):
        main = MainWindow()
        main.Show()
        return True

app = MyApp(0)
app.MainLoop()