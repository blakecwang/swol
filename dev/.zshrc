# .zshrc is for aliases and functions and runs on every terminal and
# subterminal after .zprofile

# prompt formatting
autoload -Uz vcs_info
precmd() { vcs_info }
zstyle ':vcs_info:git:*' formats '%F{green}(%b)%f'
setopt PROMPT_SUBST
PROMPT='%F{cyan}%~%f ${vcs_info_msg_0_} %# '

# NVM
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
source /Users/bwang/.goguardian

# rbenv shell wrapper function
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

# Open files in GitHub.
gho() {
  local file=$1
  if [[ -z "$file" ]]; then
    echo "Usage: ghlink <relative-file-path>"
    return 1
  fi

  # Get remote URL and clean it up
  local remote_url=$(git remote get-url origin 2>/dev/null)
  if [[ -z "$remote_url" ]]; then
    echo "Error: Not a git repository or no remote origin set."
    return 1
  fi

  # Convert SSH remote to HTTPS URL
  if [[ "$remote_url" =~ ^git@github.com: ]]; then
    remote_url=${remote_url#git@github.com:}
    remote_url=${remote_url%.git}
    remote_url="https://github.com/${remote_url}"
  else
    remote_url=${remote_url%.git}
  fi

  # Get current branch and absolute path
  local branch=$(git branch --show-current)
  local abs_path=$(realpath "$file")
  local root_dir=$(git rev-parse --show-toplevel)
  local rel_path=${abs_path#$root_dir/}

  # echo "${remote_url}/blob/${branch}/${rel_path}"
  open "${remote_url}/blob/${branch}/${rel_path}"
}

# npx shortcuts
npd() {
  if [ -z "$1" ]; then
    echo "Usage: pd <file-path>"
    return 1
  fi
  npx prettier "$1" | diff --color=always -u "$1" -
}
alias npw='npx prettier --write'
alias npt='npx playwright test'
alias nes="npx --prefix ~/.global-linter eslint -c ~/.global-linter/eslint.config.js"


# Database shortcuts
_db_run() {
    local host="$1" db="$2" pass="$3" arg="$4"

    if [ -z "$pass" ]; then
        echo "Error: password is not set." >&2
        return 1
    fi

    if [ -z "$arg" ]; then
        mariadb -A -h "$host" -u bwang -p"$pass" "$db"
    elif [ -f "$arg" ]; then
        mariadb -A -h "$host" -u bwang -p"$pass" "$db" < "$arg"
    else
        mariadb -A -h "$host" -u bwang -p"$pass" "$db" -e "$arg"
    fi
}
dba() { _db_run admin-settings.write.stg.rds.internal.goguardian.com admin_settings "$ADMIN_SETTINGS_DB_PASSWORD" "$1"; }
dbl() { _db_run liminex-ent.write.stg.rds.internal.goguardian.com liminex_ent "$LIMINEX_ENT_DB_PASSWORD" "$1"; }
dbr() { _db_run rawley.write.stg.rds.internal.goguardian.com rawley "$RAWLEY_DB_PASSWORD" "$1"; }


# Navigation
alias li='cd /liminex/'
alias gc='cd /liminex/gg4a/go-cortana/'
alias gt='cd /liminex/gg4a/tests/'
