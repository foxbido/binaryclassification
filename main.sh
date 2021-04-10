#!/usr/bin/env bash
# use `time main` to time the script.

setup_color() {
  RED=$(printf '\033[31m')    # notice, some damage operations going on
	GREEN=$(printf '\033[32m')  # finished doing
	YELLOW=$(printf '\033[33m') # running job
	BLUE=$(printf '\033[34m')   # finished shell process
	BOLD=$(printf '\033[1m')    # TODO gotta have some utilization
	RESET=$(printf '\033[m')    # reset to normal display mode
}


setup_color

if [ -d script ]; then
  cd script || exit

  # initialize the working directory by cleaning processed data directories.
  if [ -d data/corpus* ]; then
    rm -rf data/corpus*

  # prepare the index.
  if [ -f ./structure_index.py ]; then
    echo "${YELLOW}Structuring the index file with Python...${RESET}"
    chmod +x structure_index.py
    python structure_index.py
    echo "${GREEN}Done!${RESET}"
  fi

  # prepare the cluster.
  echo "${YELLOW}Shifting raw data to HDFS...${RESET}"
  echo "${RED}(This operation will overwrite '/tmp/eliot/'.)${RESET}"
  if hadoop fs -ls /tmp/eliot/; then
    hadoop fs -rm -R -skipTrash /tmp/eliot/
    hadoop fs -mkdir /tmp/eliot/
    hadoop fs -put -f ../../eliot/data /tmp/eliot/
  fi

  # building corpora.
  echo "${YELLOW}Building corpora...${RESET}"
  sleep 3s
  pig -x mapreduce build_corpora.pig
  echo "${GREEN}Done!${RESET}"
  echo "${YELLOW}Getting corpora from HDFS to local FS...${RESET}"
  hadoop fs -get /tmp/eliot/data/corpus_07s ../data/
  hadoop fs -get /tmp/eliot/data/corpus_08s ../data/
  hadoop fs -get /tmp/eliot/data/corpus_07c ../data/
  hadoop fs -get /tmp/eliot/data/corpus_08c ../data/
  echo "${GREEN}Done! You can check them in 'eliot/data/' folder.${RESET}"
  echo "${BLUE}Exiting.${RESET}"

  ########################################################################

  # run the mapreduce part on local machine and it should be fine.

fi

