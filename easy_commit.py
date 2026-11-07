import os
import subprocess
import threading

import sublime
import sublime_plugin

STATUS_KEY = 'easy_commit'
NO_CONSOLE_WINDOW = getattr(subprocess, 'CREATE_NO_WINDOW', 0)


class GitError(Exception):
    pass


def git(args, cwd):
    try:
        result = subprocess.run(
            ['git'] + args, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding='utf-8', errors='replace',
            creationflags=NO_CONSOLE_WINDOW)
    except OSError as e:
        raise GitError('Could not run git: {}'.format(e))
    if result.returncode != 0:
        output = result.stderr.strip() or result.stdout.strip()
        raise GitError('git {} failed.\n\n{}'.format(args[0], output))
    return result.stdout


class EasyCommitAllCommand(sublime_plugin.TextCommand):
    def paths(self):
        return []

    def run(self, edit):
        threading.Thread(target=self.prepare).start()

    def prepare(self):
        try:
            repo = self.repo_root()
            self.show_status('Pulling...')
            git(['pull'], repo)
            if not git(['status', '--porcelain', '--'] + self.paths(), repo).strip():
                self.finish('Nothing to commit.')
                return
        except GitError as e:
            self.fail(str(e))
            return
        sublime.set_timeout(lambda: self.ask_message(repo))

    def repo_root(self):
        file_name = self.view.file_name()
        candidates = [os.path.dirname(file_name)] if file_name else []
        candidates += self.view.window().folders()
        for folder in candidates:
            try:
                return git(['rev-parse', '--show-toplevel'], folder).strip()
            except GitError:
                pass
        raise GitError('The current file or folder is not inside a Git repository.')

    def ask_message(self, repo):
        self.show_status('Type the commit message (Esc cancels)')
        self.view.window().show_input_panel(
            'Commit message:', '',
            lambda message: threading.Thread(target=self.commit, args=(repo, message)).start(),
            None,
            lambda: self.finish('Commit canceled.'))

    def commit(self, repo, message):
        if not message.strip():
            self.finish('Commit canceled.')
            return
        paths = self.paths()
        try:
            git(['add', '-A', '--'] + paths, repo)
            git(['commit', '-m', message, '--'] + paths, repo)
            self.show_status('Pushing...')
            git(['push'], repo)
        except GitError as e:
            self.fail(str(e))
            return
        self.finish('Pushed: ' + message)

    def show_status(self, message):
        sublime.set_timeout(lambda: self.view.set_status(STATUS_KEY, 'EasyCommit: ' + message))

    def finish(self, message):
        self.show_status(message)
        sublime.set_timeout(lambda: self.view.erase_status(STATUS_KEY), 5000)

    def fail(self, message):
        def show():
            self.view.erase_status(STATUS_KEY)
            sublime.error_message('EasyCommit\n\n' + message)
        sublime.set_timeout(show)


class EasyCommitFileCommand(EasyCommitAllCommand):
    def paths(self):
        return [self.view.file_name()]

    def is_enabled(self):
        return self.view.file_name() is not None
