#!/usr/bin/zsh

export ZDOT=$HOME/.z
export ZUSER=$HOME/.zu

if ! [[ -d $ZUSER ]]; then
  mkdir $ZUSER
fi

zstyle ':completion:*' range 1000:100
setopt autocd
setopt auto_list
setopt auto_menu

export HISTFILE=$HOME/.zhistory
export HISTSIZE=10000000
export SAVEHIST=10000000

setopt BANG_HIST
setopt EXTENDED_HISTORY
setopt INC_APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_ALL_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_IGNORE_SPACE
setopt HIST_SAVE_NO_DUPS
setopt HIST_REDUCE_BLANKS
setopt HIST_VERIFY

# import aliases
. $ZDOT/aliases.sh

# Sourcing custom files
if [[ -f $ZUSER/.aliases ]]; then
  . $ZUSER/.aliases
fi

if [[ -d $HOME/.local/bin ]]; then
    export PATH=$HOME/.local/bin:$PATH
fi

if [[ -d $HOME/.bin ]]; then
    export PATH=$HOME/.bin:$PATH
fi

# Loading plugins
if [[ -d $ZUSER/plugins ]]; then

fi

# Source prompt style
source $ZDOT/prompts/prompt-simple.sh

if [[ -f $ZUSER/zinit ]]; then
  . $ZUSER/zinit
fi

