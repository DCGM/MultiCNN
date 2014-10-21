# Creates configuration files for caffe

DEF_DIR=./definitions/

for DEF in `ls "$DEF_DIR"`
do
    NET_DIR="./NETS/$DEF"
    mkdir -p "$NET_DIR"

    BODY=`./prepareNet.sh <"$DEF_DIR/$DEF"`
    LAST_TOP=`echo "$BODY" | sed -e 's/^[ \t]*//' | grep top: |tail -n 1| cut -f 2 -d \ `

    (
        cat train_val_start
        echo "$BODY"
        cat train_val_end | sed "s/bottom:$/bottom: $LAST_TOP/"
    ) > "$NET_DIR/net_train_val.prototxt"
#    (
#        cat val_start
#        echo "$BODY"
#        cat val_end | sed "s/bottom:$/bottom: $LAST_TOP/"
#    ) > "$NET_DIR/net_val.prototxt"

    cp net_solver.prototxt "$NET_DIR"

done
