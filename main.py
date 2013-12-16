import sublime, sublime_plugin, os

settings = {}

def plugin_loaded():
    global settings
    settings = sublime.load_settings("FileComplete.sublime-settings")

class FileComplete(sublime_plugin.EventListener):

    # def on_selection_modified_async(self,view):
    #     if not view.window():
    #         return

    #     sel = view.sel()[0].a
    #     completionPath = self.get_completion_path(view, sel)
    #     if completionPath:
    #         print(completionPath)
    #         _files = [ _file for _file in os.listdir(completionPath) if not _file.startswith('.')]
    #         if(len(_files) > 0):
    #             view.run_command('auto_complete',
    #                 {'disable_auto_insert': True, 'next_completion_if_showing': False})

    def get_completion_path(self,view,sel):
        scope_contents = view.substr(view.extract_scope(sel-1))
        completionPath = scope_contents.replace('\r\n', '\n').split('\n')[0]
        if completionPath.startswith(("'","\"","(")):
            completionPath = completionPath[1:-1]

        if completionPath.startswith("~"):
            completionPath = os.path.expanduser(completionPath)

        if not completionPath.startswith(('/', './', '../', '~/')):
            return False
        return completionPath[:completionPath.rfind('/')+1] if '/' in completionPath else ''

    def on_query_completions(self, view, prefix, locations):
        sel = view.sel()[0].a
        completionPath = self.get_completion_path(view, sel)

        if not completionPath or not view.file_name():
            return

        viewDir = os.path.split(view.file_name())[0]
        viewDir = os.path.join(viewDir, completionPath)

        completions = []

        try:
            files = os.listdir(viewDir)

            for f in files:
                if f.startswith('.'): continue
                if os.path.isdir(viewDir + f):
                    f += '/'
                completions.append((f, f))
            if completions:
                return completions
        except OSError:
            return

