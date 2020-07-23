#!/bin/bash


help(){

echo 
}

kill_consumner(){
    pid_file="consumer/.pid"
    if [ -f $pid_file ];then
      pid=`cat $pid_file`
      sudo kill -9 $pid
      rm -rf $pid_file
    fi
}

kill_web_server(){
    pid_file="web/.pid"
    if [ -f $pid_file ];then
      pid=`cat $pid_file`
      sudo kill -9 $pid
      rm -rf $pid_file
    fi
}

kill_all()
{
  for pid_file in "consumer/.pid" "web/.pid"; do

    if [ -f $pid_file ];then
      pid=`cat $pid_file`
      sudo kill -9 $pid
      rm -rf $pid_file
    fi

  done
}


consumer(){


PORT=9001
DRAW_INTERVAL=30

while getopts "pd" opt; do

  shift

  case "$opt" in
    p)
      
      PORT=$1
      
    ;;
    d)
      DRAW_INTERVAL=$2
    ;;
  esac
done

  python main.py consumer --port $PORT --draw $DRAW_INTERVAL 1>/dev/null &

  echo $! > consumer/.pid
}

all(){
  consumer
  web_server
}

web_server()
{

  PORT=9002

  while getopts "p" opt; do

    shift

    case "$opt" in
      p)
        
        PORT=$1
      ;;
    esac
  done

  python main.py web --port $PORT >/dev/null 2>&1 &

  echo $! > web/.pid
}

chat(){

  python main.py chat

}

test(){
  python -m unittest test.py 
}

kill_server(){

  case $1 in 
    consumer)
      kill_consumner
    ;;

    web_server)
      kill_web_server
    ;;
    *)
        kill_all
    ;;
  esac
}


main(){

  COMMAND=$1

  if [ $# -gt 1 ];then

  shift

  fi

  case $COMMAND in

    all)
        all
    ;;

    consumer)
      consumer $@
    ;;

    web_server)
      web_server $@
    ;;

    chat)
      chat
    ;;

    kill)
      kill_server $@
    ;;
    test)

      test
      
    ;;

    *)
      help
    ;;

  esac
}

main $@



