import sublime
import sublime_plugin
import subprocess
import threading
import os

class EasyCommitAllCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        threading.Thread(target=self.easy_commit_all).start()

    def easy_commit_all(self):
        working_dir = self.view.window().extract_variables()['folder']
        self.update_status('Performing fetch...')

        if self.run_git_command(['git', 'fetch'], working_dir):
            self.update_status('Fetch successfully completed!')
            if self.run_git_command(['git', 'pull'], working_dir) and self.check_for_changes(working_dir):
                if self.run_git_command(['git', 'add', '-A'], working_dir):
                    sublime.set_timeout(lambda: self.request_commit_message(working_dir), 0)
                else:
                    self.display_error_message("Failed to add changes.")
            else:
                self.display_error_message("Failed to perform the pull.")
        else:
            self.display_error_message("Failed to perform the fetch.")

    def request_commit_message(self, working_dir):
        self.update_status("Awaiting commit message...")
        self.view.window().show_input_panel(
            "Commit Message:", "", 
            lambda s: self.commit(s, working_dir), None, 
            lambda: self.cancel_commit(working_dir))

    def commit(self, message, working_dir):
        if message:
            self.update_status('Commit message received!')
            if not self.run_git_command(['git', 'commit', '-m', message], working_dir):
                self.display_error_message("Failed to perform the commit.")
                return

            self.update_status('Sending your changes...')
            if not self.run_git_command(['git', 'push'], working_dir):
                self.display_error_message("Failed to send changes.")
                return

            self.update_status('Success!')
            sublime.set_timeout(self.erase_status, 5000)
        else:
            self.cancel_commit(working_dir)

    def cancel_commit(self, working_dir):
        self.update_status("Commit canceled.")
        self.undo_add(working_dir)
        sublime.set_timeout(self.erase_status, 5000)

    def undo_add(self, working_dir):
        self.run_git_command(['git', 'reset'], working_dir)

    def check_for_changes(self, working_dir):
        try:
            output = subprocess.check_output(['git', 'status', '--porcelain'], cwd=working_dir)
            return len(output.strip()) > 0
        except subprocess.CalledProcessError as e:
            self.display_error_message(f"Error checking for changes: {e}")
            return False

    def run_git_command(self, command, working_dir):
        try:
            subprocess.check_output(command, cwd=working_dir)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def display_error_message(self, message):
        sublime.error_message(message)
        self.erase_status()

    def update_status(self, message):
        sublime.set_timeout(lambda: self.view.set_status('easy_commit', message), 0)

    def erase_status(self):
        sublime.set_timeout(lambda: self.view.erase_status('easy_commit'), 0)

class EasyCommitFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        threading.Thread(target=self.easy_commit_file).start()

    def easy_commit_file(self):
        working_dir = self.view.window().extract_variables()['folder']
        file_name = self.view.file_name()

        if file_name:
            self.update_status('Performing fetch...')
            if self.run_git_command(['git', 'fetch'], working_dir):
                self.update_status('Fetch successfully completed!')
                if self.run_git_command(['git', 'diff', '--quiet', file_name], working_dir):
                    self.display_error_message("No changes detected in the current file.")
                else:
                    if self.run_git_command(['git', 'add', file_name], working_dir):
                        sublime.set_timeout(lambda: self.request_commit_message(working_dir), 0)
                    else:
                        self.display_error_message("Failed to add current file.")
            else:
                self.display_error_message("Failed to perform the fetch.")
        else:
            self.display_error_message("No file selected.")

    def request_commit_message(self, working_dir):
        self.update_status("Awaiting commit message...")
        self.view.window().show_input_panel(
            "Commit Message:", "", 
            lambda s: self.commit(s, working_dir), None, 
            lambda: self.cancel_commit(working_dir))

    def commit(self, message, working_dir):
        if message:
            self.update_status('Commit message received!')
            if not self.run_git_command(['git', 'commit', '-m', message], working_dir):
                self.display_error_message("Failed to perform the commit.")
                return

            self.update_status('Sending your changes...')
            if not self.run_git_command(['git', 'push'], working_dir):
                self.display_error_message("Failed to send changes.")
                return

            self.update_status('Success!')
            sublime.set_timeout(self.erase_status, 5000)
        else:
            self.cancel_commit(working_dir)

    def cancel_commit(self, working_dir):
        self.update_status("Commit canceled.")
        self.undo_add(working_dir)
        sublime.set_timeout(self.erase_status, 5000)

    def undo_add(self, working_dir):
        self.run_git_command(['git', 'reset'], working_dir)

    def check_for_changes(self, working_dir):
        try:
            output = subprocess.check_output(['git', 'status', '--porcelain'], cwd=working_dir)
            return len(output.strip()) > 0
        except subprocess.CalledProcessError as e:
            self.display_error_message(f"Error checking for changes: {e}")
            return False

    def run_git_command(self, command, working_dir):
        try:
            subprocess.check_output(command, cwd=working_dir)
            return True
        except subprocess.CalledProcessError as e:
            return False

    def display_error_message(self, message):
        sublime.error_message(message)
        self.erase_status()

    def update_status(self, message):
        sublime.set_timeout(lambda: self.view.set_status('easy_commit', message), 0)

    def erase_status(self):
        sublime.set_timeout(lambda: self.view.erase_status('easy_commit'), 0)
