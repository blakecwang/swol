# The following lines were added by Docker Desktop to add commands to your PATH.
export PATH="$PATH:/Users/bwang/.docker/bin"
# End of Docker Desktop section.

# .zprofile is for exporting environment variables and runs
# once on login, before .zshrc


# Homebrew environment setup
eval "$(/opt/homebrew/bin/brew shellenv zsh)"

# Add rbenv shims to the beginning of your PATH
export PATH="/Users/bwang/.rbenv/shims:${PATH}"
export RBENV_SHELL=zsh

# Load local secrets if the file exists
if [ -f "$HOME/.secrets" ]; then
    source "$HOME/.secrets"
fi

export GO_CORTANA_PRETTY_LOGS=1
export GO_CORTANA_LOG_TO_FILE=1
