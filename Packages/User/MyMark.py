import sublime, sublime_plugin

def get_cursor(init_cursor, sel):
    if init_cursor.a != sel.a:
        return sublime.Region(sel.a, sel.a)
    else:
        return sublime.Region(sel.b, sel.b)

class ClearMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.run_command("clear_bookmarks", {"name": "mark"})
        self.view.settings().set('with_marker', False)

class DoAfterMarkCommand(sublime_plugin.TextCommand):
    def run(self, edit, command, args = {}):
        self.view.run_command("clear_mark")
        self.view.run_command(command)

class SetMarkCommand(sublime_plugin.TextCommand):
    cursors = []
    def run(self, edit):
        mark = self.view.get_regions("mark")
        if mark and mark[0] != self.view.sel()[0]:
            new_sel = []
            for i in range(len(SetMarkCommand.cursors)):
                new_sel.append(get_cursor(SetMarkCommand.cursors[i], self.view.sel()[i]))
            sublime.status_message("%s %s %s" % (SetMarkCommand.cursors, self.view.sel(), new_sel))
            self.view.run_command("clear_mark")
            self.view.sel().clear()
            for s in new_sel:
                self.view.sel().add(s)
        if self.view.get_regions("mark"):
            self.view.run_command("clear_mark")
        else:
            SetMarkCommand.cursors = []
            for s in self.view.sel():
                SetMarkCommand.cursors.append(s)
            mark = [s for s in self.view.sel()]
            self.view.add_regions("mark", mark, "mark", "dot",
                sublime.HIDDEN | sublime.PERSISTENT)
            self.view.settings().set('with_marker', True)
            sublime.status_message("Cursor: %s" % (SetMarkCommand.cursors))

class MarkDetector(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        mark = view.get_regions("mark")
        if mark:
            view.run_command("select_to_mark")

    def on_modified(self, view):
        mark = view.get_regions("mark")
        if mark:
            view.run_command("clear_mark")
