#!/bin/bash

get_name() {
    case $1 in
        0) echo 'Иван' ;;
        1) echo 'Степан' ;;
        2) echo 'Евгений' ;;
        3) echo 'Сергей' ;;
        4) echo 'Андрей' ;;
        5) echo 'Павел' ;;
        6) echo 'Руслан' ;;
        7) echo 'Даниил' ;;
        8) echo 'Михаил' ;;
        9) echo 'Станислав' ;;
        *) echo 'Иван' ;;
    esac
}

get_fam() {
    case $1 in
        0) echo 'Иванов' ;;
        1) echo 'Смирнов' ;;
        2) echo 'Кузнецов' ;;
        3) echo 'Попов' ;;
        4) echo 'Васильев' ;;
        5) echo 'Петров' ;;
        6) echo 'Соколов' ;;
        7) echo 'Михайлов' ;;
        8) echo 'Новиков' ;;
        9) echo 'Фёдоров' ;;
        *) echo 'Иванов' ;;
    esac
}

get_random_nm() {
    n=$(($RANDOM % 9))
    f=$(($RANDOM % 9))
    echo $(get_name $n) $(get_fam $f)
}

chr() {
  [ "$1" -lt 256 ] || return 1
  printf "\\$(printf '%03o' "$1")"
}

get_stud_num() {
    head=$((1 + $RANDOM % 99))
    mid=$(chr $(shuf -i 65-67 -n 1))
    tail=$((1 + $RANDOM % 999))
    echo $head$mid$tail
}


for (( i=0; i<$1; i++));
do 
    redis-cli set $(get_stud_num) "$(get_random_nm)"
done