import sublime, sublime_plugin

class DeleteLineCommand(sublime_plugin.TextCommand):
    delete_line_sequence = False
    def _is_delete_all_string(self):
        point = self.view.sel()[0].begin()
        region = self.view.line(point)
        return region.a == region.b

    def _delete_to_eol(self):
        self.view.run_command("move_to", {"to": "eol", "extend": True})
        deleted_str = self.view.substr(self.view.sel()[0])
        self.view.run_command("right_delete")
        if self._is_delete_all_string:
            self.view.run_command("right_delete")
            deleted_str = deleted_str + "\n" # self.view.line_endings()
        return deleted_str

    def run(self, edit, forward = True):
        sublime.status_message("%s" % str(delete_line_sequence))
        if forward:
            deleted_str = self._delete_to_eol()
            if delete_line_sequence:
                sublime.set_clipboard(sublime.get_clipboard() + deleted_str)
            else:
                sublime.set_clipboard(deleted_str)
                delete_line_sequence = True
        else:
            self.view.run_command("run_macro_file", {"file": "Packages/Default/Delete to BOL.sublime-macro"})

class DeleteLineDetector(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        DeleteLineCommand.delete_line_sequence = False

    def on_modified(self, view):
        DeleteLineCommand.delete_line_sequence = False
