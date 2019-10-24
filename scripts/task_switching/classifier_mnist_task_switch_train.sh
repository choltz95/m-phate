if [ $# -lt 1 ]; then
    DATA_DIR="./data"
else
    DATA_DIR=$1
fi

EXTRA_ARGS=$2

mkdir -p ${DATA_DIR}/task_switch
for scheme in task domain class; do
    for optimizer in adam adagrad; do
        python scripts/task_switching/classifier_mnist_task_switch_train.py ${EXTRA_ARGS} --optimizer $optimizer --save-dir ${DATA_DIR} $scheme &
        python scripts/task_switching/classifier_mnist_task_switch_train.py ${EXTRA_ARGS} --optimizer $optimizer --rehearsal 5000 --save-dir ${DATA_DIR} $scheme &
    done
done
wait
