#!/usr/bin/zsh

# Function and aliases
function vn () {
    if [[ -f $1/bin/activate ]]; then
      . $1/bin/activate
    fi
}

export EDITOR=vim

alias @zshrc="$EDITOR $HOME/.zshrc"
alias @zr="clear ; exec zsh"
alias @aliases="$EDITOR $ZUSER/.aliases"

alias ls="ls --color=yes"
alias la="ls -A"
alias ll="ls -lAh"
alias l="ls -lh"
alias vim=nvim
alias tmux="tmux -f $HOME/.config/tmux.conf"

