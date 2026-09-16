# The following lines were added by Docker Desktop to add commands to your PATH.
export PATH="$PATH:/Users/bwang/.docker/bin"
# End of Docker Desktop section.

eval "$(/opt/homebrew/bin/brew shellenv zsh)"
eval export PATH="/Users/bwang/.rbenv/shims:${PATH}"
export RBENV_SHELL=zsh
command rbenv rehash 2>/dev/null
rbenv() {
  local command
  command="${1:-}"
  if [ "$#" -gt 0 ]; then
    shift
  fi

  case "$command" in
  rehash|shell)
    eval "$(rbenv "sh-$command" "$@")";;
  *)
    command rbenv "$command" "$@";;
  esac
}

# NPM Token
export NPM_TOKEN="npm_<REDACTED>"
