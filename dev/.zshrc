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

# Database shortcuts
alias dba="mariadb -A -h admin-settings.write.stg.rds.internal.goguardian.com -u bwang -p'<REDACTED>' admin_settings"
alias dbl="mariadb -A -h liminex-ent.write.stg.rds.internal.goguardian.com -u bwang -p'<REDACTED>' liminex_ent"

# Navigation
alias li='cd /liminex/'
alias gc='cd /liminex/gg4a/go-cortana/'
