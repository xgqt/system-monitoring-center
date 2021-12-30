#!/usr/bin/env python3

# ----------------------------------- MainMenusGUI - Main Menus GUI Import Function (contains import code of this module in order to avoid running them during module import) -----------------------------------
def main_menus_gui_import_func():

    global Gtk, os

    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk
    import os


    global Config
    import Config

    global MainGUI
    import MainGUI


    # Import gettext module for defining translation texts which will be recognized by gettext application. These lines of code are enough to define this variable if another values are defined in another module (MainGUI) before importing this module.
    global _tr                                                                                # This arbitrary variable will be recognized by gettext application for extracting texts to be translated
    from locale import gettext as _tr


# ----------------------------------- MainMenusGUI - Main Menus GUI Function (the code of this module in order to avoid running them during module import and defines GUI functions/signals) -----------------------------------
def main_menus_gui_func():

    # Define builder and get all objects (Main Menu GUI and About Dialog) from GUI file.
    builder = Gtk.Builder()
    builder.add_from_file(os.path.dirname(os.path.realpath(__file__)) + "/../ui/MainMenusDialogs.ui")


    # ********************** Define object names for Main Menu GUI and About Dialog **********************
    global menu1001m
    global menuitem1004m, menuitem1005m, menuitem1006m, checkmenuitem1001m

    global aboutdialog1001d

    # ********************** Get objects for Main Menu GUI and About Dialog **********************
    menu1001m = builder.get_object('menu1001m')
    menuitem1004m = builder.get_object('menuitem1004m')
    menuitem1005m = builder.get_object('menuitem1005m')
    menuitem1006m = builder.get_object('menuitem1006m')
    checkmenuitem1001m = builder.get_object('checkmenuitem1001m')

    aboutdialog1001d = builder.get_object('aboutdialog1001d')


    # ********************** Define object functions for Main Menu GUI **********************
    def on_menu1001m_show(widget):
        checkmenuitem1001m.disconnect_by_func(on_checkmenuitem1001m_toggled)                  # Disconnect "on_checkmenuitem1001m_toggled" function in order to prevent it from sending event signals when toggling is performed by the code for reflecting the user preference about "Floating Window".
        if Config.show_floating_summary == 0:
            checkmenuitem1001m.set_active(False)
        if Config.show_floating_summary == 1:
            checkmenuitem1001m.set_active(True)
        checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)

    def on_checkmenuitem1001m_toggled(widget):                                                # "Floating Summary" menu item
        if "FloatingSummary" not in globals():                                                # Floating Summary window might have been opened on the application start and user may want to hide it from the Main Menu of the application. Existance check of the "FloatingSummary" variable is performed before the "if checkmenuitem1001m.get_active() == False:" statement in order to avoid errors of FloatingSummary not defined.
            global FloatingSummary
            import FloatingSummary
        if checkmenuitem1001m.get_active() == True:
            FloatingSummary.floating_summary_import_func()
            FloatingSummary.floating_summary_gui_func()
            FloatingSummary.window3001.show()                                                 # Window has to be shown before running loop thread of the Floating Summary window. Because window visibility data is controlled to continue repeating "floating_summary_thread_run_func" function.
            FloatingSummary.floating_summary_thread_run_func()
            Config.show_floating_summary = 1
        if checkmenuitem1001m.get_active() == False:
            FloatingSummary.window3001.hide()
            Config.show_floating_summary = 0
        Config.config_save_func()

    def on_menuitem1004m_activate(widget):                                                    # "Settings" menu item
        if "SettingsGUI" not in globals():                                                    # Settings module is imported and the following functions are run only one time during application run. This statement is used in order to avoid them running on every window opening.
            global SettingsGUI
            import SettingsGUI
            SettingsGUI.settings_gui_import_func()
            SettingsGUI.settings_gui_func()
        SettingsGUI.window2001.show()

    def on_menuitem1005m_activate(widget):                                                    # "About" menu item
        try:
            software_version = open(os.path.dirname(os.path.abspath(__file__)) + "/__version__").readline()
        except:
            pass
        aboutdialog1001d.set_version(software_version)
        aboutdialog1001d.run()
        aboutdialog1001d.hide()

    def on_menuitem1006m_activate(widget):                                                    # "Quit" menu item
        Gtk.main_quit()


    # ********************** Connect signals to GUI objects for Main Menu GUI **********************
    menu1001m.connect("show", on_menu1001m_show)
    checkmenuitem1001m.connect("toggled", on_checkmenuitem1001m_toggled)
    menuitem1004m.connect("activate", on_menuitem1004m_activate)
    menuitem1005m.connect("activate", on_menuitem1005m_activate)
    menuitem1006m.connect("activate", on_menuitem1006m_activate)


# ----------------------------------- MainMenusGUI - Main Menu GUI System Default Terminal Detection Error Dialog Function (shows a warning dialog when a startup item is tried to be reset to system default which means user specific desktop file of the startup application will be deleted (system-wide values file will be untouched)) -----------------------------------
def main_menus_gui_system_default_terminal_detection_error_dialog():

    error_dialog1001 = Gtk.MessageDialog(transient_for=MainGUI.window1, title=_tr("Error"), flags=0, message_type=Gtk.MessageType.ERROR,
    buttons=Gtk.ButtonsType.CLOSE, text=_tr("Default Terminal Application Not Detected"), )
    error_dialog1001.format_secondary_text(_tr("Default terminal application on this system could not be detected."))
    error_dialog1001.run()
    error_dialog1001.destroy()
