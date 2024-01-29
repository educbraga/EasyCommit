# EasyCommit

**EasyCommit: Effortless Git commits in Sublime Text for Developers who want to ship more.**

## Overview
EasyCommit simplifies the process of making Git commits, allowing developers to focus more on coding and less on version control management.

## Features
After pressing a single key binding:
- **Automated Git Workflow**: The plugin performs a series of Git operations: fetch, pull, and add all.
- **Commit Messages**: After staging changes, it prompts for a commit message.
- **Committing**: Commits with the provided message and then pushes the changes to the remote repository on the current branch.
- **Status Updates**: Provides ongoing feedback in the Sublime Text status bar, keeping you informed at every step.
- **Error Handling**: Displays error messages in case of any issues during the Git operations.
- **Cancellation Option**: Allows cancelling the commit process by pressing ESC.

## Installation
EasyCommit can be installed via Package Control in Sublime Text. Simply search for "EasyCommit" and install it directly within your editor. Alternatively, you can download the .py file and place it in Sublime Text > Settings > Browse Packages > User.

## Usage
After installation, configure a keybinding to trigger the plugin:
1. Open `Preferences > Key Bindings` in Sublime Text.
2. Add a keybinding for the command `git_workflow`:

   ```json
   { "keys": ["your_preferred_shortcut"], "command": "easy_commit" }
   ```

Replace your_preferred_shortcut with your desired key combination.

Once set up, use this shortcut to activate EasyCommit in any Git-enabled project.

## Contributing

Contributions to EasyCommit are welcome! If you have suggestions, bug reports, or want to contribute code, please feel free to open an issue or submit a pull request.

## Support

For support, questions, or feature requests, please open an issue in this repository.

## License

MIT
