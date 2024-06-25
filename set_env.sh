#!/bin/bash

if [ ! -f .env ]; then
  echo "Файл .env не найден!"
  exit 1
fi

while IFS='=' read -r key value; do
  if [[ $key =~ ^#.*$ || -z $key ]]; then
    continue
  fi
  key=$(echo $key | xargs)
  value=$(echo $value | xargs)
  export "$key=$value"
done < .env

echo "Установленные переменные окружения:"
env
