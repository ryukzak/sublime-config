import sublime, sublime_plugin

# TODO: Add support for multiple selection

delete_line_sequence = False
cursor = None

class DeleteLineCommand(sublime_plugin.TextCommand):
    def _on_empty_string(self):
        point = self.view.sel()[0].begin()
        region = self.view.line(point)
        return region.empty()

    def _delete_to_eol(self):
        self.view.run_command("move_to", {"to": "eol", "extend": True})
        deleted_str = self.view.substr(self.view.sel()[0])
        self.view.run_command("right_delete")
        if self._on_empty_string():
            self.view.run_command("right_delete")
            deleted_str = deleted_str + "\n" # self.view.line_endings()
        elif deleted_str == "":
            deleted_str = "\n"
        return deleted_str

    def run(self, edit, forward = True):
        global delete_line_sequence, cursor
        if forward:
            deleted_str = self._delete_to_eol()
            if delete_line_sequence:
                sublime.set_clipboard(sublime.get_clipboard() + deleted_str)
            else:
                delete_line_sequence = True
                cursor = self.view.sel()[0]
                sublime.set_clipboard(deleted_str)
        else:
            self.view.run_command("run_macro_file", {"file": "Packages/Default/Delete to BOL.sublime-macro"})

class DeleteLineDetector(sublime_plugin.EventListener):
    def on_selection_modified(self, view):
        global delete_line_sequence, cursor
        if delete_line_sequence and cursor != view.sel()[0]:
            delete_line_sequence = False

    def on_modified(self, view):
        global delete_line_sequence, cursor
        if delete_line_sequence and cursor != view.sel()[0]:
            delete_line_sequence = False
