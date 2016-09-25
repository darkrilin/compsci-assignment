import wx, wx.html
import sys


class MainWindow(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Neuroscience Graph Maker", pos=(150,150), size=(1200,700))
        # Initialise the UI
        self.InitUI()

    def InitUI(self):
        # Create the status bar
        self.CreateStatusBar()
        # Initialise the menu bar
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

        self.SettingsItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="&Settings", help="Edit Application Settings")
        self.FileMenu.AppendItem(self.SettingsItem)

        self.FileMenu.AppendSeparator()

        self.ImportItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="&Import", help="Import MATLAB data")
        self.FileMenu.AppendItem(self.ImportItem)

        self.ExportAsItem = wx.MenuItem(self.FileMenu, wx.ID_ANY, text="&Export as...", help="Open the export dialog to export data")
        self.FileMenu.AppendItem(self.ExportAsItem)

        self.FileMenu.AppendSeparator()

        self.PrintItem = wx.MenuItem(self.FileMenu, wx.ID_PRINT, help="Print the data")
        self.FileMenu.AppendItem(self.PrintItem)

        self.FileMenu.AppendSeparator()

        self.ExitItem = wx.MenuItem(self.FileMenu, wx.ID_EXIT, text="&Exit\tCtrl+Q")
        self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), self.ExitItem.GetId())]))
        self.FileMenu.AppendItem(self.ExitItem)

        self.MenuBar.Append(self.FileMenu, "&File")

        # Edit Menu
        self.EditMenu = wx.Menu()

        self.UndoItem = wx.MenuItem(self.EditMenu, wx.ID_UNDO)
        self.EditMenu.AppendItem(self.UndoItem)

        self.RedoItem = wx.MenuItem(self.EditMenu, wx.ID_ANY, text='&Redo\tCtrl+Y', help="Redo last action")
        self.SetAcceleratorTable(wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Y'), self.RedoItem.GetId())]))
        self.EditMenu.AppendItem(self.RedoItem)

        self.EditMenu.AppendSeparator()

        self.CutItem = wx.MenuItem(self.EditMenu, wx.ID_CUT)
        self.EditMenu.AppendItem(self.CutItem)

        self.CopyItem = wx.MenuItem(self.EditMenu, wx.ID_COPY)
        self.EditMenu.AppendItem(self.CopyItem)

        self.PasteItem = wx.MenuItem(self.EditMenu, wx.ID_PASTE)
        self.EditMenu.AppendItem(self.PasteItem)

        self.DeleteItem = wx.MenuItem(self.EditMenu, wx.ID_DELETE)
        self.EditMenu.AppendItem(self.DeleteItem)

        self.MenuBar.Append(self.EditMenu, "&Edit")

        # View Menu
        self.ViewMenu = wx.Menu()

        self.ZoomInItem = wx.MenuItem(self.ViewMenu, wx.ID_ZOOM_IN)
        self.ViewMenu.AppendItem(self.ZoomInItem)

        self.ZoomOutItem = wx.MenuItem(self.ViewMenu, wx.ID_ZOOM_OUT)
        self.ViewMenu.AppendItem(self.ZoomOutItem)

        self.MenuBar.Append(self.ViewMenu, "&View")

        # Set the menu bar
        self.SetMenuBar(self.MenuBar)
        # Bind events to menu items
        self.Bind(wx.EVT_MENU, self.OnNew, self.NewItem)
        self.Bind(wx.EVT_MENU, self.OnOpen, self.OpenItem)
        self.Bind(wx.EVT_MENU, self.OnSave, self.SaveItem)
        self.Bind(wx.EVT_MENU, self.OnSaveAs, self.SaveAsItem)
        self.Bind(wx.EVT_MENU, self.OnSettings, self.SettingsItem)
        self.Bind(wx.EVT_MENU, self.OnImport, self.ImportItem)
        self.Bind(wx.EVT_MENU, self.OnExportAs, self.ExportAsItem)
        self.Bind(wx.EVT_MENU, self.OnPrint, self.PrintItem)
        self.Bind(wx.EVT_MENU, self.OnExit, self.ExitItem)
        self.Bind(wx.EVT_MENU, self.OnUndo, self.UndoItem)
        self.Bind(wx.EVT_MENU, self.OnRedo, self.RedoItem)
        self.Bind(wx.EVT_MENU, self.OnCut, self.CutItem)
        self.Bind(wx.EVT_MENU, self.OnCopy, self.CopyItem)
        self.Bind(wx.EVT_MENU, self.OnPaste, self.PasteItem)
        self.Bind(wx.EVT_MENU, self.OnDelete, self.DeleteItem)

    def OnNew(self, e):
        print("New")

    def OnOpen(self, e):
        print("Open")

    def OnSave(self, e):
        print("Save")

    def OnSaveAs(self, e):
        print("SaveAs")

    def OnSettings(self, e):
        print("Settings")

    def OnImport(self, e):
        print("Import")

    def OnExportAs(self, e):
        print("ExportAs")

    def OnPrint(self, e):
        print("Print")

    def OnExit(self, e):
        self.Close()

    def OnUndo(self, e):
        print("Undo")

    def OnRedo(self, e):
        print("Redo")

    def OnCut(self, e):
        print("Cut")

    def OnCopy(self, e):
        print("Copy")

    def OnPaste(self, e):
        print("Paste")

    def OnDelete(self, e):
        print("Delete")

class MyApp(wx.App):
    def OnInit(self):
        main = MainWindow()
        main.Show()
        return True

app = MyApp(0)
app.MainLoop()