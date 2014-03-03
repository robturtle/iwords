# Filename: INSTALL.sh
# Author:   LIU Yang
# Create Time: Thu Mar 3 11:31:13 HKT 2014
# License:     LGPL v2.0+
# Contact Me:  JeremyRobturtle@gmail.com
# Brief: Prepare the database and make the plan

./readgre.py < gre.txt
./readtoefl.py < toefl.txt
./scheduler.py
