#!/bin/bash

awk '
          /:$/{
            flag=""
          }
          /containers/{
            flag=1
          }
          flag && NF && (/image:/){
            match($0,/^[[:space:]]+/);
            val=substr($0,RSTART,RLENGTH);
            $NF="'$1':'$2'";
            print val $0;
            next
          }
          1
          '   deployment.yaml > tmp && mv tmp deployment.yaml

          git config --global user.email "incredibletoken@gmail.com"
          git config --global user.name "incredibletoken"
          git add .
          git commit -m "updated docker tag in kubernetes manifest to version '$2'"
          git push origin HEAD:master
