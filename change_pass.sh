#!/bin/bash

(echo $1; echo $2; echo $2) | smbpasswd -r $4 -U $3