#!/usr/bin/env zsh

setup_color() {
  RED=$(printf '\033[31m')    # notice, some damage operations going on
	GREEN=$(printf '\033[32m')  # finished doing
	YELLOW=$(printf '\033[33m') # running job
	BLUE=$(printf '\033[34m')   # finished shell process
	BOLD=$(printf '\033[1m')    # TODO gotta have some utilization
	RESET=$(printf '\033[m')    # reset to normal display mode
}

tf_idf_07c(){

    # corpus_07c
    echo "${GREEN}phase1 of ${RESET}${YELLOW}corpus_07c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_1.py -reducer tf-idf/reducer_1.py \
    -input ../data/corpus_07c \
    -output ../data/tmp/phase1_07c

    echo "${GREEN}phase2 of ${RESET}${YELLOW}corpus_07c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_2.py -reducer tf-idf/reducer_2.py \
    -input ../data/tmp/phase1_07c \
    -output ../data/tmp/phase2_07c

    echo "${GREEN}phase3 of ${RESET}${YELLOW}corpus_07c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_3.py -reducer tf-idf/reducer_3.py \
    -input ../data/tmp/phase2_07c \
    -output ../data/corpus_07c_tf-idf

    echo "${BLUE}cleaning shit of 07c...${RESET}"
    rm -r ../data/tmp/*07c
    echo "${GREEN}tf-idf of corpus_07c done!${RESET}"

}


tf_idf_08c(){

    # corpus_08c
    echo "${GREEN}phase1 of ${RESET}${YELLOW}corpus_08c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_1.py -reducer tf-idf/reducer_1.py \
    -input ../data/corpus_08c \
    -output ../data/tmp/phase1_08c

    echo "${GREEN}phase2 of ${RESET}${YELLOW}corpus_08c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_2.py -reducer tf-idf/reducer_2.py \
    -input ../data/tmp/phase1_08c \
    -output ../data/tmp/phase2_08c

    echo "${GREEN}phase3 of ${RESET}${YELLOW}corpus_08c...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_3.py -reducer tf-idf/reducer_3.py \
    -input ../data/tmp/phase2_08c \
    -output ../data/corpus_08c_tf-idf

    echo "${BLUE}cleaning shit of 08c...${RESET}"
    rm -r ../data/tmp/*08c
    echo "${GREEN}tf-idf of corpus_08c done!${RESET}"

}


tf_idf_07s(){

    # corpus_07s
    echo "${GREEN}phase1 of ${RESET}${YELLOW}corpus_07s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_1.py -reducer tf-idf/reducer_1.py \
    -input ../data/corpus_07s \
    -output ../data/tmp/phase1_07s

    echo "${GREEN}phase2 of ${RESET}${YELLOW}corpus_07s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_2.py -reducer tf-idf/reducer_2.py \
    -input ../data/tmp/phase1_07s \
    -output ../data/tmp/phase2_07s

    echo "${GREEN}phase3 of ${RESET}${YELLOW}corpus_07s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_3.py -reducer tf-idf/reducer_3.py \
    -input ../data/tmp/phase2_07s \
    -output ../data/corpus_07s_tf-idf

    echo "${BLUE}cleaning shit of 07s...${RESET}"
    rm -r ../data/tmp/*07s
    echo "${GREEN}tf-idf of corpus_07s done!${RESET}"

}


tf_idf_08s(){

    # corpus_08s
    echo "${GREEN}phase1 of ${RESET}${YELLOW}corpus_08s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_1.py -reducer tf-idf/reducer_1.py \
    -input ../data/corpus_08s \
    -output ../data/tmp/phase1_08s

    echo "${GREEN}phase2 of ${RESET}${YELLOW}corpus_08s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_2.py -reducer tf-idf/reducer_2.py \
    -input ../data/tmp/phase1_08s \
    -output ../data/tmp/phase2_08s

    echo "${GREEN}phase3 of ${RESET}${YELLOW}corpus_08s...${RESET}"
    hadoop jar tf-idf/hadoop-streaming-3.0.0.jar \
    -mapper tf-idf/mapper_3.py -reducer tf-idf/reducer_3.py \
    -input ../data/tmp/phase2_08s \
    -output ../data/corpus_08s_tf-idf

    echo "${BLUE}cleaning shit of 08s...${RESET}"
    rm -r ../data/tmp/*08s
    echo "${GREEN}tf-idf of corpus_08s done!${RESET}"

}


main() {

    setup_color

    # clear shits of others
    rm -r ../data/tmp/

    tf_idf_07c & tf_idf_08c & tf_idf_07s & tf_idf_08s

    # till all sub-process finish
    wait

    # clear your own shits
    rm -r ../data/tmp/

}

main
