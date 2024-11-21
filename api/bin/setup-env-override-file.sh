#!/usr/bin/env bash
# setup-env-override-file.sh
#
# Generate an override.env file
# with secrets pre-populated for local development.
#
# Examples:
#   ./setup-env-override-file.sh
#   ./setup-env-override-file.sh --recreate
#

set -o errexit -o pipefail

PROGRAM_NAME=$(basename "$0")

CYAN='\033[96m'
GREEN='\033[92m'
RED='\033[01;31m'
END='\033[0m'

USAGE="Usage: $PROGRAM_NAME [OPTION]

  --recreate         Recreate the override.env file, fully overwriting any existing file
"

main() {
  print_log "Running $PROGRAM_NAME"

  for arg in "$@"
  do
    if [ "$arg" == "--recreate" ]; then
      recreate=1
    else
      echo "$USAGE"
      exit 1
    fi
  done

  OVERRIDE_FILE="override.env"

  if [ -f "$OVERRIDE_FILE" ] ; then
    if [ $recreate ] ; then
      print_log "Recreating existing override.env file"
    else
      print_log "override.env already exists, not recreating"
      exit 0
    fi
  fi

  # Delete any key files that may be leftover from a prior run
  cleanup_files

  # Generate RSA keys
  # note ssh-keygen generates a different format for
  # the public key so we run it through openssl to fix it
  ssh-keygen -t rsa -b 2048 -m PEM -N '' -f tmp_jwk.key 2>&1 >/dev/null
  openssl rsa -in tmp_jwk.key -pubout -outform PEM -out tmp_jwk.pub

  PUBLIC_KEY=`cat tmp_jwk.pub`
  PRIVATE_KEY=`cat tmp_jwk.key`

  cat > $OVERRIDE_FILE <<EOF
# override.env
#
# Any environment variables written to this file
# will take precedence over those defined in local.env
#
# This file will not be checked into github and it is safe
# to store secrets here, however you should still follow caution
# with using any secrets locally if they cause the app to interact
# with external systems.
#
# This file was generated by running:
#    make setup-env-override-file
#
# Which runs as part of our "make init" flow.
#
# If you would like to re-generate this file, please run:
#    make setup-env-override-file args="--recreate"
#
# Note that this will completely erase any existing configuration you may have

############################
# Authentication
############################

API_JWT_PRIVATE_KEY="$PRIVATE_KEY"

API_JWT_PUBLIC_KEY="$PUBLIC_KEY"
EOF


  print_log "Created new override.env"

  # Cleanup all keys generated in this run
  cleanup_files
}

# Cleanup a single file if it exists
cleanup_file()
{
  FILE=$1
  shift;

  if [ -f "$FILE" ] ; then
    rm "$FILE"
  fi
}

# Cleanup all miscellaneous keys generated
cleanup_files()
{
  cleanup_file tmp_jwk.key
  cleanup_file tmp_jwk.pub
  cleanup_file tmp_jwk.key.pub
}

print_log() {
  printf "$CYAN%s $GREEN%s: $END%s\\n" "$(date "+%Y-%m-%d %H:%M:%S")" "$PROGRAM_NAME" "$*"
}

# Entry point
main "$@"