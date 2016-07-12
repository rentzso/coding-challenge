#!/bin/bash

# this files uses a simpler implementation of the solution to generate the list of rolling medians for testing

GRADER_ROOT=$(dirname ${BASH_SOURCE})

function generate_output {
  TEST_FOLDERS=$(ls ${GRADER_ROOT}/tests)

  # Loop through all tests
  for test_folder in ${TEST_FOLDERS}; do
    echo ${test_folder}
    full_path=${GRADER_ROOT}/tests/${test_folder}
    cat ${full_path}/venmo_input/venmo-trans.txt | python ../unit_tests/tracker_util.py > ${full_path}/venmo_output/output.txt
  done
}

generate_output
