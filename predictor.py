import csv
from prettytable import PrettyTable
import plotly.express as px
import pandas as pd

def predicted_position(rows,name):
    r=[]
    k=[]
    z=PrettyTable()
    for i in rows:
        if i[0] == 'EPL' and i[1] == '2019':
            tn = i[3]
            matches = float(i[4])
            rating = float(i[18])
            xGD = float(i[23])
            xPTS = float(i[27])
            eospts = int(((xPTS/matches)*38))
            eosgd =  round(((xGD/matches)*38)+rating)
            r.append([tn,eospts,eosgd])
    #print(r)
    k=sorted(r, key=lambda x: (x[1], x[2]), reverse=True)
    #print(k)
    n=0
    z.field_names=['Team','Points','GD']
    for i in k:
        z.add_row(i)
        n=n+1
        if i[0] == name:
            print("Projected End of Season Rank: ",n)
            print("Projected End of Season Points: ",i[1])
            print("Projected End of Season GD: ", i[2])
    print("Projected End of Season Table: ")
    print(z)

def team(name):
    rows=[]
    rows1=[]
    x=PrettyTable()
    y=PrettyTable()
    z=PrettyTable()
    flag=0
    with open('data/epl_player_understat.csv','r') as us:
        with open('data/EPL_teams.csv','r') as cs :
            team_data = csv.reader(cs)
            for row in team_data:
                rows.append(row)
            #print(rows)
            #prints team stats from 2014 to 2019
            x.field_names=rows[0]
            y.field_names=rows[0]
            pos=0
            wins = 0
            matches=0
            rating = 0
            xG = 0
            xGA = 0
            xGD = 0
            xPTS = 0
            for i in rows:
                if i[3] == name:
                    t_name = name
                    x.add_row(i)
                    if i[1] == '2019':
                        flag=1
                        y.add_row(i)

            print(t_name)
            if flag == 1:
                print("Current Season:")
                print(y)

            print("Historical EPL Record: ")
            print(x)

            if flag == 0:
                print("No current season data as team has been relegated.")
                return

            if flag == 1:
                understat = csv.reader(us)
                for row in understat:
                    rows1.append(row)
                z.field_names=rows1[0]
                for i in rows1:
                    if i[3] == name:
                        if i[0] == '2019':
                            z.add_row(i)
                print("Current Season Player data: ")
                z.sortby = "Goals"
                z.reversesort = True
                print(z)
                predicted_position(rows,name)

def player(name):
    rows = []
    rows1 = []
    rows2 = []
    rows3 = []
    rows4 = []
    r = []
    goals = 0
    assists = 0
    xG = 0
    xA = 0
    xG90 = 0
    xA90 = 0
    SpG = 0
    pp = 0
    x = PrettyTable()
    y = PrettyTable()
    z = PrettyTable()
    flag=0
    with open('data/epl_player_understat.csv', 'r') as us:
        with open('data/epl_player_whoscored.csv', 'r') as ws:
            whoscored = csv.reader(ws)
            for row in whoscored:
                rows.append(row)
            understat = csv.reader(us)
            for row in understat:
                #print(row[8:14])
                rows1.append(row)
            #print(rows1)
            rows2.append(rows[0])
            for i in rows:
                if i[2] ==  name:
                    rows2.append(i)

            rows3.append(rows1[0])
            for i in rows1:
                if i[2] == name:
                    rows3.append(i)
            #print(rows3)
            for i in rows3:
                r.append(i[8:14])
            #print(r)
            #print(rows2)
            #rows4.append(rows2+r)
            #print(rows4)
            n=0
            for i in rows2:
                    j=r[n]
                    rows4.append(i+j)
                    n=n+1
            #print(rows4)
            x.field_names=rows4[0]
            y.field_names=rows4[0]
            for i in rows4:
                if i[2] == name:
                    x.add_row(i)
                    if i[0] == '2019':
                        flag=1
                        y.add_row(i)
                        #use these vaiables to make the spider chart
                        goals = (i[8])
                        assists = (i[9])
                        xG = (i[17])
                        xA = (i[19])
                        xG90 = i[21]
                        xA90 = i[22]
                        #SpG = float(i[12])
                        #pp = float(i[13])
            if flag ==1:
                print("Current Season Data: ")
                print(y)


            print("Historical data: ")
            print(x)

            if flag == 0:
                print("This player does not play in the premier league anymore")
                return

            #spider chart but doesnt come properly for some reason
            df = pd.DataFrame(dict(
                r=[goals, assists, xG, xA, xG90, xA90],
                theta=['Goals', 'Assists', 'xG',
                       'xA', 'xG90', 'xA90']))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            fig.show()



n = input("Enter: player or team")
if n=="player":
    name = input("Enter player name")
    player(name)
elif n=="team":
    name = input("Enter team name")
    team(name)
else:
    print("Invalid input")
    exit()

		# 	<!-- <script type = "text/javascript">
		# 	var x = document.getElementById('x')
        #
		# 	for(var i=1;i<=20;i++){
		# 		var tr = document.createElement('TR')
        #
		# 			for(var j=1;j<=20;j++){
		# 				var td = document.createElement('TD')
		# 				td.appendChild(document.createTextNode("{{team["+j+"]}}"))
		# 				tr.appendChild(td)
        #
		# 			}x.appendChild(tr)
		# 		// x.innerHTML +=  "<td> {{ season[i]["+i+"] }} </td>
	    #   // <td> {{ position[i]["+i+"] }} </td>
		# 		// <td> {{ team["+i+"] }} </td>
		# 		// <td> {{ matches["+i+"] }} </td>
		# 		// <td> {{ wins["+i+"] }} </td>
		# 		// <td> {{ draws["+i+"] }} </td>
		# 		// <td> {{ loses["+i+"] }} </td>
		# 		// <td> {{ goals["+i+"] }} </td>
		# 		// <td> {{ gA["+i+"] }} </td>
		# 		// <td> {{ gD["+i+"] }} </td>
		# 		// <td> {{ points["+i+"] }} </td>"
		# }
		# </script> -->
