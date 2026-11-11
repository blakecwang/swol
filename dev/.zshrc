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
stg-dba() { _db_run admin-settings.write.stg.rds.internal.goguardian.com admin_settings "$STG_ADMIN_SETTINGS_DB_PASSWORD" "$1"; }
stg-dbl() { _db_run liminex-ent.write.stg.rds.internal.goguardian.com liminex_ent "$STG_LIMINEX_ENT_DB_PASSWORD" "$1"; }
stg-dbr() { _db_run rawley.write.stg.rds.internal.goguardian.com rawley "$STG_RAWLEY_DB_PASSWORD" "$1"; }
stg-dbx() { _db_run x3.write.stg.rds.internal.goguardian.com x3 "$STG_X3_DB_PASSWORD" "$1"; }
stg-dbe() { _db_run app-ext.write.stg.rds.internal.goguardian.com liminex_ent "$STG_APP_EXT_DB_PASSWORD" "$1"; }
stg-dbp() { _db_run panther.write.stg.rds.internal.goguardian.com panther "$STG_PANTHER_DB_PASSWORD" "$1"; }

prd-dba() { _db_run admin-settings.read.prod.rds.internal.goguardian.com admin_settings "$PRD_ADMIN_SETTINGS_DB_PASSWORD" "$1"; }
prd-dbl() { _db_run liminex-ent.read.prod.rds.internal.goguardian.com liminex_ent "$PRD_LIMINEX_ENT_DB_PASSWORD" "$1"; }
prd-dbr() { _db_run rawley.read.prod.rds.internal.goguardian.com rawley "$PRD_RAWLEY_DB_PASSWORD" "$1"; }
prd-dbx() { _db_run x3.read.prod.rds.internal.goguardian.com x3 "$PRD_X3_DB_PASSWORD" "$1"; }
prd-dbp() { _db_run panther.read.prod.rds.internal.goguardian.com panther "$STG_PANTHER_DB_PASSWORD" "$1"; }

# won't be there forever
prd-dbx-snapshot() { _db_run x3-db-snapshot-10-19-26-apettit.crnsmyryvp1u.us-west-2.rds.amazonaws.com x3 "$PRD_X3_DB_PASSWORD" "$1"; }

# grep: skip node_modules on recursive searches (-r / -R)
alias grep='grep --color=auto --exclude-dir=node_modules'

# find: prune node_modules automatically
find() {
  local -a opts paths expr
  # leading BSD find options (-H -L -P -E -X -d -s -x)
  while [[ $1 == -[HLPEXdsx] ]]; do opts+=("$1"); shift; done
  # paths come before the expression
  while (( $# )) && [[ $1 != -* && $1 != '!' && $1 != '(' ]]; do paths+=("$1"); shift; done
  (( ${#paths} )) || paths=(.)
  expr=("$@")

  if (( ${#expr} == 0 )); then
    command find "${opts[@]}" "${paths[@]}" -name node_modules -prune -o -print
  elif (( ${expr[(I)-(print|print0|exec|execdir|ok|delete|ls|fprint)]} )); then
    # the expression already has an action, so don't add -print
    command find "${opts[@]}" "${paths[@]}" -name node_modules -prune -o \( "${expr[@]}" \)
  else
    command find "${opts[@]}" "${paths[@]}" -name node_modules -prune -o \( "${expr[@]}" \) -print
  fi
}


# find/replace
find-replace() {
  find . -type f -not -path '*/.*' -exec sed -i '' "s/$1/$2/g" {} +
}


# Check deps coverage (/liminex/data-infra/cicd/check-deps-coverage/script/README.md)
# check-deps-coverage gg4a/rooney          # check only
# check-deps-coverage --fix gg4a/rooney    # check, then update Deps
check-deps-coverage() {
  local fix="" svc root="${LIMINEX:-$HOME/liminex}"
  while [ $# -gt 0 ]; do
    case "$1" in
      --fix) fix="--fix" ;;
      *) svc="${1%/}"; svc="${svc%/cicd.toml}" ;;
    esac
    shift
  done
  [ -n "$svc" ] || { echo "usage: check-deps-coverage [--fix] <service-dir>   e.g. check-deps-coverage gg4a/rooney" >&2; return 1; }
  [ -f "$root/$svc/cicd.toml" ] || { echo "no cicd.toml at $root/$svc" >&2; return 1; }

  docker run --rm \
    --cap-add=SYS_PTRACE --security-opt seccomp=unconfined \
    -v "$root":/liminex -w /liminex \
    -v cdc-gomod:/go/pkg/mod -v cdc-gobuild:/root/.cache/go-build \
    -e CGO_ENABLED=0 -e GOFLAGS=-buildvcs=false \
    golang:1.26.3-alpine3.23 \
    sh -c "apk add --no-cache strace git build-base >/dev/null &&
      go run /liminex/data-infra/cicd/check-deps-coverage/script trace \
        --cicd-toml /liminex/$svc/cicd.toml \
        --dir /liminex/$svc \
        $fix \
        -- /liminex/golang/gotest.sh"
}


# Navigation
alias li='cd /liminex/'
alias gc='cd /liminex/gg4a/go-cortana/'
alias gt='cd /liminex/gg4a/tests/'
alias pl='cd ~/proglog/'

# scratchpad
alias sp='vi ~/scratch/main.go'
alias sr='(cd ~/scratch && go run .)'


eval "$(mise activate zsh)"


# Full-text search of Claude Code session transcripts, newest first.
# Usage: claude-search <term>   then: claude --resume <session-id>
claude-search() {
  if [[ -z "$1" ]]; then
    echo "usage: claude-search <term>" >&2
    return 1
  fi
  local f
  grep -rli --include='*.jsonl' -- "$1" ~/.claude/projects 2>/dev/null \
    | grep -v '/subagents/' \
    | while read -r f; do printf '%s\t%s\n' "$(stat -f %m "$f")" "$f"; done \
    | sort -rn | cut -f2- \
    | while read -r f; do
        printf '%s  %s  %s\n' "$(stat -f %Sm -t '%Y-%m-%d %H:%M' "$f")" "${f:t:r}" "${f:h:t}"
        printf '    %s\n\n' "$(jq -r 'select(.type=="user" and (.message.content|type)=="string" and (.message.content|startswith("<")|not)) | .message.content' "$f" 2>/dev/null \
          | head -1 | cut -c1-100)"
      done
}

owner() {
  local file
  file=$(grep -rlE --include=cicd.toml "^Name = ['\"]$1['\"]" /liminex/ | head -1)
  if [[ -z "$file" ]]; then
    echo "No cicd.toml found with Name '$1'"
    return 1
  fi
  grep -E '^Owner' "$file" | cut -d= -f2 | tr -d " '\"" | grep . || echo "Owner not found in $file"
}


####### REFERENCE #######

# Get the sha of the merge commit for a pr
# gh pr view <pr-number> --json mergeCommit

# Check if commit is ancestor of another
# git merge-base --is-ancestor <maybe-ancestor-commit> <descendant-commit>
# echo $?    0: true, 1: false

# x3 prod write
# mariadb -A -h x3.write.prod.rds.internal.goguardian.com -u x3master -p"$PRD_X3_DB_WRITE_PASSWORD" x3
