#!/usr/bin/env bash
## Define DIV first
#set($DIV = '################################################################################')
#set($title = 'section')

#macro(header $title)
${DIV}
# $title
${DIV}
#end
/usr/bin/tput reset
printf '\e[3J'

${DIV}
# ${FILE_NAME}
# Author: Shane Young
# Date: ${YEAR}-${MONTH}-${DAY}
# Revision:	1.0
# Platform: MacOS
#
# Description
# ${Description}
#
# Versions
# 1.	Features
#
${DIV}
# Exit Codes
#
${DIV}

#header ('Environment setup')
#[[
# Global Variables
BASEPATH="$(dirname $0)"
BASENAME="$(basename $0)"

# Create temporary and working directory
WRKDIR="$TMPDIR"
TMPDIR="/tmp/$BASENAME."$(openssl rand -hex 12)
/bin/mkdir -p -m 777 "$TMPDIR"

# Turn off line wrapping:
#printf '\033[?7l'
# Turn on  line wrapping:
#printf '\033[?7h'

# Set window size ex. 100w x 40h
#printf '\033[8;40;100t'

# Set window Title
printf "\033]0;${BASENAME%%.*}\007"

# Hide the cursor for the run of the script
/usr/bin/tput civis
]]#

#header ('Traps')
#[[
function exit_trap() {
    # Restore the cursor
	/usr/bin/tput cnorm
}
trap exit_trap TERM INT EXIT
]]#

#header ('Functions')
#[[
# Function to print text in colour
function colour() {
    local DATE=$(date +"%Y-%m-%dT%H:%M:%S")
    local COLOUR_CODE="$1"
    shift
    local LEVEL="$1"
    shift
    local MESSAGE="$*"
    printf "\033[%sm%s [ %-9s] %s \033[0m\n" "${COLOUR_CODE}" "$DATE" "${LEVEL}" "$MESSAGE"
}

# Function for logging
function logging.debug() {
    colour "90" DEBUG "$(printf "${@}")"
}

function logging.info() {
    colour "92" INFO "$(printf "${@}")"
}

function logging.warning() {
    colour "93" WARNING "$(printf "${@}")"
}

function logging.error() {
    colour "91" ERROR "$(printf "${@}")"
}

function logging.critical() {
    colour "97;41" CRITICAL "$(printf "${@}")"
    exit 1
}

]]#


#header ('Arguments')

#[[
while getopts "p:m:t:bh" OPT; do
    case $OPT in
    b)
        PARAMETER_B=true
        ;;
    p)
        PARAMETER_P="${OPTARG}"
        ;;
    m)
        PARAMETER_M="${OPTARG}"
        ;;
    t)
        PARAMETER_T="${OPTARG}"
        ;;
    h)
        HELP=true
        ;;
    \?)
        echo "Invalid option: -$OPTARG" >&2
        exit 1
        ;;
    :)
        echo "Option -$OPTARG requires an argument." >&2
        exit 1
        ;;
    esac
done
]]#

#header ('Help')

#[[
if ${HELP:-false}; then
    echo "Usage: ${BASENAME} [options]

    Options:
      -b          Enable the 'b' parameter (flag, no argument).
      -p <value>  Set the 'p' parameter to <value>.
      -m <value>  Set the 'm' parameter to <value>.
      -t <value>  Set the 't' parameter to <value>.
      -h          Show this help message and exit.

    Examples:
      ${BASENAME} -b                 # Enable 'b' parameter
      ${BASENAME} -p my_value        # Set 'p' to 'my_value'
      ${BASENAME} -m 123 -t 456      # Set 'm' to '123' and 't' to '456'
      ${BASENAME} -h                 # Display this help message
    "
    exit
fi
]]#

#header ('Main')
#[[
logging.debug "debug message"
logging.info "info message"
for var in ${!PARAMETER_*}; do
    logging.info "$var=${!var}"
done
logging.warning "warning message"
logging.error "error message"
logging.critical "critical message"

exit 0
]]#