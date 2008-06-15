"""
Gisto - Gitso is to support others

Gitso is a utility to facilitate the connection of VNC

@author: Aaron Gerber ('gerberad')
@author: Derek Buranen ('burner') <derek@buranen.info>
@copyright: 2007-2008
"""

import pygtk
pygtk.require('2.0')
import gtk, os, signal, webbrowser, sys

class Connect(object):
    """
    ??????
    
    @author: Derek Buranen
    @author: Aaron Gerber
    """
    
    #TODO: Test Try using the pretty python decorator instead of calling the class. Not sure GTK will support this but worth a try
    ## @gtk.about_dialog_set_url_hook ##
    def openURL(func, url):
        """
        Makes sure the URLs are clickable
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        webbrowser.open_new(url)

    gtk.about_dialog_set_url_hook(openURL)
    

    # Callback: radioToggle
     #               : EVENT - Radio buttons toggled
    def radioToggle(self, widget, data=None):
        """
        Toggles Radio Buttons
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        value = (data, ("OFF", "ON")[widget.get_active()])
        if value[0] == "_Get Help":
            if value[1] == "ON":
                self.GetSupportEntry.set_sensitive(True)
                self.GetSupportEntry.grab_focus()
        elif value[0] == "Give _Support":
            if value[1] == "ON":
                self.GetSupportEntry.set_sensitive(False)
    
    
    # Callback: connectSupport
    #               : EVENT - Connect button was pressed
    def connectSupport(self, widget, data=None):
        """
        ???
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        if self.GetSupportRadio.get_active()  == True:
            self.connectButton.set_sensitive(False)
            self.stopButton.set_sensitive(True)
            self.statusLabel.set_text(self.statusLabelText[1])
            self.returnPID = os.spawnlp(os.P_NOWAIT, 'x11vnc', 'x11vnc', '-connect' , '%s' % self.GetSupportEntry.get_text())
        else:
            self.connectButton.set_sensitive(False)
            self.stopButton.set_sensitive(True)
            self.statusLabel.set_text(self.statusLabelText[1])
            self.returnPID = os.spawnlp(os.P_NOWAIT, 'vncviewer', 'vncviewer', '-listen')

    
    # Callback: showAbout
    #               : EVENT - About Gitso selected
    def showAbout(self, widget, data=None):
        """
        Display About Dialog
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        license = open(os.path.join(sys.path[0], '..', 'share', 'doc', 'gitso', 'copyright'), 'r')
        aboutDialog = gtk.AboutDialog()
        aboutDialog.set_name("Gitso")
        aboutDialog.set_version("0.4")
        aboutDialog.set_authors(["Derek Buranen", "Aaron Gerber"])
        aboutDialog.set_license(license.read())
        aboutDialog.set_website('http://gitso.googlecode.com')
        aboutDialog.set_copyright("2007-2008 Derek Buranen, Aaron Gerber")
        aboutDialog.set_comments("Gitso Is To Support Others")
        license.close()
        aboutDialog.run()
        aboutDialog.destroy()

    
    # Callback: getClipboard
    #               : EVENT - Paste menu item selected
    def getClipboard(self, menu, data=None):
        """
        Paste clipboard text in Support Entry Field
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        self.GetSupportEntry.set_text(self.clipboard.wait_for_text())
        return

    
    # Callback: getClipboard
    #               : EVENT - Copy menu item selected
    def setClipboard(self, menu, data=None):
        """
        Set the value of the clipboard
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        self.clipboard.set_text(self.GetSupportEntry.get_text())
        return

        
    # Callback: killPID
    #               : EVENT - Stop is pressed or Applications ends
    def killPID(self, data=None):
        """
        Kill VNC instance
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        if self.returnPID != 0:
            self.connectButton.set_sensitive(True)
            self.stopButton.set_sensitive(False)
            os.kill(self.returnPID, signal.SIGKILL)
            self.statusLabel.set_text(self.statusLabelText[0])
            self.returnPID = 0
        return


    # Callback: deleteEvent
    #               : EVENT - "Close" option is selected - title bar or button
    
    #TODO: Add "Close" button
    #TODO: "quit" prompt dialog
    #TODO: Close VNC connection
    def deleteEvent(self, widget, event, data=None):
        """
        Close Window
        
        If you return FALSE in the "deleteEvent" signal handler,
        GTK will emit the "destroy" signal. Returning TRUE means
        you don't want the window to be destroyed.
        This is useful for popping up 'are you sure you want to quit?' dialog
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        print "Close Window"
        return False
        
        
    # Callback: destroy
    #               : EVENT - Gtk_widget_destroy() is called on the window, or return FALSE in "deleteEvent"
    def destroy(self, widget, data=None):
        """
        Quit Application
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        print "Quit Application"
        self.killPID(self)
        gtk.main_quit()


    # Run Loop: Initilize program
    def __init__(self):
        """
        Setup Application Dialog
        
        @author: Derek Buranen
        @author: Aaron Gerber
        """
        #initializing various variables
        self.returnPID = 0
        self.statusLabelText = ('Status: Idle', 'Status: Started')
        
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Gitso")
        self.window.connect("delete_event", self.deleteEvent)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(0)
        self.window.set_icon_from_file(os.path.join(sys.path[0], '..', 'share', 'gitso', 'gitso.svg'))
        
        self.clipboard = gtk.clipboard_get(gtk.gdk.SELECTION_CLIPBOARD)

        ui = '''<ui>
            <menubar name="MenuBar">
            <menu action="File">
            <menuitem action="Quit"/>
            </menu>
            <menu action="Edit">
            <menuitem action="Copy"/>
            <menuitem action="Paste"/>
            </menu>
            <menu action="Help">
            <menuitem action="About"/>
            </menu>
            </menubar>
            </ui>'''
    
        # Create a UIManager instance
        GitsoUIManager = gtk.UIManager()
            
        # Add the accelerator group to the toplevel window
        AccelGroup = GitsoUIManager.get_accel_group()
        self.window.add_accel_group(AccelGroup)
    
        # Create an ActionGroup
        self.ActionGroup = gtk.ActionGroup('GitsoUIManager')
    
        # Create actions
        self.ActionGroup.add_actions([('Quit', gtk.STOCK_QUIT, '_Quit', None, 'Quit the Program', self.destroy),
                     ('File', None, '_File'),
                     ('Copy', gtk.STOCK_COPY, '_Copy', None, 'Copy IP Address', self.setClipboard),
                     ('Paste', gtk.STOCK_PASTE, '_Paste', None, 'Copy IP Address', self.getClipboard),
                     ('Edit', None, '_Edit'),
                     ('About', gtk.STOCK_ABOUT, '_About', None, 'About Gitso', self.showAbout),
                     ('Help', None, '_Help')])
        self.ActionGroup.get_action('Quit').set_property('short-label', '_Quit')
    
        # Add the ActionGroup to the GitsoUIManager
        GitsoUIManager.insert_action_group(self.ActionGroup, 0)
    
        # Add a UI description
        GitsoUIManager.add_ui_from_string(ui)
    
        # Create a MenuBar
        menubar = GitsoUIManager.get_widget('/MenuBar')
       
        # Initialize IP Textbox
        self.GetSupportEntry = gtk.Entry(50)
        self.GetSupportEntry.set_text("IP address")
        self.GetSupportEntry.show()

        # Initialize Radio Buttons.
        self.GiveSupportRadio = gtk.RadioButton(None, "Give _Support", use_underline=True)
        self.GetSupportRadio  = gtk.RadioButton(self.GiveSupportRadio, "_Get Help", use_underline=True)
        
        self.GiveSupportRadio.connect("toggled", self.radioToggle, "Give _Support")
        self.GetSupportRadio.connect("toggled", self.radioToggle, "_Get Help")
        
        self.GetSupportRadio.set_active(True)
        self.GiveSupportRadio.show()
        self.GetSupportRadio.show()

        #TODO: Connect Button -- Default
        #### ToDo :: Connect Button -- Default ##########
        #self.button.grab_default()
        ####################################
        # Initialize Connect Button Bar
        self.connectButton = gtk.Button("OK", gtk.STOCK_CONNECT)
        self.connectButton.connect("clicked", self.connectSupport)
        self.connectButton.show()
        self.stopButton = gtk.Button("Stop", gtk.STOCK_STOP)
        self.stopButton.connect("clicked", self.killPID)
        self.stopButton.set_sensitive(False)
        self.stopButton.show()
        self.statusLabel = gtk.Label(self.statusLabelText[0])
        self.statusLabel.show()


        # Initialize Boxes
        self.mainVBox            =  gtk.VBox(False, 0)
        self.interfaceVBox      = gtk.VBox(False, 0)
        self.menuHBox           = gtk.HBox(False, 0)
        self.getSupportHBox  = gtk.HBox(False, 0)
        self.giveSupportHBox = gtk.HBox(False, 0)
        self.buttonHBox          = gtk.HBox(False, 0)


        # VBox MenuBar
        self.menuHBox.pack_start(menubar, True, True, 0)
        self.mainVBox.pack_start(self.menuHBox, False, False, 0)
        
        # VBox cell 1
        self.getSupportHBox.pack_start(self.GetSupportRadio, True, True, 8)
        self.getSupportHBox.pack_start(self.GetSupportEntry, True, True, 8)
        self.interfaceVBox.pack_start(self.getSupportHBox, True, True, 4)

        # VBox cell 2
        self.giveSupportHBox.pack_start(self.GiveSupportRadio, True, True, 8)
        self.interfaceVBox.pack_start(self.giveSupportHBox, True, True, 0)

        # VBox cell 3
        self.buttonHBox.pack_start(self.statusLabel, False, False, 8)
        self.buttonHBox.pack_end(self.stopButton, False, False, 8)
        self.buttonHBox.pack_end(self.connectButton, False, False, 8)
        self.interfaceVBox.pack_start(self.buttonHBox, False, False, 0)

        # Show main window and initialize focus
        self.GetSupportEntry.grab_focus()
        self.mainVBox.pack_end(self.interfaceVBox, False, False, 8)

        self.mainVBox.show()
        self.interfaceVBox.show()
        self.menuHBox.show()
        self.getSupportHBox.show()
        self.giveSupportHBox.show()
        self.buttonHBox.show()
        
        self.window.add(self.mainVBox)
        self.window.set_position(gtk.WIN_POS_CENTER)
        self.window.show()

    # Run Loop: Main run loop
    def main(self):
        gtk.main()