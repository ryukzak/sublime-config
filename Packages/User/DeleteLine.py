import sublime, sublime_plugin

class DeleteLineCommand(sublime_plugin.TextCommand):
    def run(self, edit, forward = True):
        if forward:
            self.view.run_command("run_macro_file", {"file": "Packages/Default/Delete to EOL.sublime-macro"})
            point = self.view.sel()[0].begin()
            region = self.view.line(point)
            if region.a == region.b:
                self.view.run_command("right_delete")
        else:
            self.view.run_command("run_macro_file", {"file": "Packages/Default/Delete to BOL.sublime-macro"})
