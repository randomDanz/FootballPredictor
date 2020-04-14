from flask import Flask,render_template,url_for,request
import csv
from prettytable import PrettyTable
import plotly.express as px
import pandas as pd
from flask_paginate import Pagination, get_page_args
from flask import jsonify
from flask_cors import CORS

app=Flask(__name__)
CORS(app)
cors = CORS(app, resources = {
    r"/*" : {
        "origins":"*"
    }
})

@app.route("/")
def hello():
    return render_template('home.html')



@app.route("/displayData", methods=["POST","GET"])
def dispData():
    if request.method == "POST":
        str = request.form['search']
        infile1 = open("data/epl_player_understat.csv","r")
        infile2 = open("data/epl_player_whoscored.csv","r")
        infile3 = open("data/EPL_teams.csv","r")

        #print(str,type(str))

        for line in infile3:
            row = line.split(",")

            if row[3].lower() == str.lower():
                print(row[3],type(row[3]))
                q = team(str)
                #print("q is ",type(q))
                # for item in q:
                #     print(item)
                #print("Q ------->> ", q[len(q)-3][1], type(q[len(q)-2][1]))
                if (q[len(q)-3][1] == '2019'):
                    return render_template('displayData.html', q = q, len = len(q))
                else:
                    return render_template('displayDataAlt.html', q = q, len = len(q))


        for line in infile1:
            row = line.split(",")

            if(row[2].lower() == str.lower()):
                q = player(str)
                print(q,type(q))
                return render_template('displayPlayer.html' , pD = q , len = len(q))

        str = "No team or Player could be found, Try Again!"
        return render_template('home.html', str = str)

def get_users(i,players,offset=0, per_page=10):
    return players[i][offset: offset + per_page]

@app.route("/players")
def play():

    players = [[],[],[],[],[],[],[],[],[],[]]
    pagination_users = [[],[],[],[],[],[],[],[],[],[]]
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')

    infile1 = open("data/epl_player_understat.csv","r")
    infile2 = open("data/epl_player_whoscored.csv","r")


    i=0
    for line in infile2:
        row = line.split(",")
        #print(row[2], type(row[2]))
        temp=row[0]
        #print(temp, type(temp))
        if(temp=='2019'):
            #print(row[2], type(row[2]))
            players[i].append(row[2]) #Name
            i+=1
            players[i].append(row[3]) #Team
            i+=1
            players[i].append(row[5]) #position
            i+=1
            players[i].append(row[6]) #Appearences
            i+=1
            players[i].append(row[7]) #Minutes
            i+=1
            players[i].append(row[8]) #Goals
            i+=1
            players[i].append(row[9]) #Assists
            i+=1
            players[i].append(row[16]) #Rating
            i+=1
        i=0

    i=8
    players[8]=[None] * len(players[0])
    players[9]=[None] * len(players[0])
    for line in infile1:
        row = line.split(",")
        temp=row[0]
        temp2=row[2]
        try:
            indx=players[0].index(temp2)
        except ValueError:
            continue
        else:
            #print(temp, type(temp)
            if(temp=='2019'):
                players[i][indx] = row[8] #xG
                i+=1
                players[i][indx] = row[10] #xA
                i+=1
            i=8

    total = len(players[9])
    print(total)

    for i in range(0,10):
        pagination_users[i] = get_users(i,players,offset=offset, per_page=per_page)

    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    print(pagination)
    return render_template('players.html',
                           users=pagination_users,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

def createtable(year):
    infile = open("data/EPL_teams.csv","r")
    season=list()
    position=list()
    team=[]
    matches=[]
    wins=[]
    draws=[]
    loses=[]
    goals=[]
    gA=[]
    gD=[]
    points=[]
    for line in infile:
        row = line.split(",")
        temp=row[1]
        #print(temp, type(temp)
        if(temp==year):
            season.append(row[1])
            position.append(row[2])
            team.append(row[3])
            matches.append(row[4])
            wins.append(row[5])
            draws.append(row[6])
            loses.append(row[7])
            goals.append(row[8])
            gA.append(row[9])
            gD.append(row[10])
            points.append(row[11])

    infile.close()
    return render_template('table.html',row = row, season = season, position = position, team = team, matches = matches, wins = wins, draws = draws, loses = loses, goals = goals, gA = gA, gD = gD, points = points)


@app.route("/table")
def table():
    return createtable('2019')

@app.route("/table-1")
def table1():
    return createtable('2018')

@app.route("/table-2")
def table2():
    return createtable('2017')

@app.route("/table-3")
def table3():
    return createtable('2016')

@app.route("/table-4")
def table4():
    return createtable('2015')

@app.route("/table-5")
def table5():
    return createtable('2014')


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
    return(k)

def team(name):
    rows=[]
    rows1=[]
    returnlist=[]
    temp=[]
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
                    returnlist.append(i)
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
                understat = csv.reader(us)
                for row in understat:
                    rows1.append(row)
                for i in rows1:
                    if i[3] == name:
                        temp.append(i)
                returnlist.append(temp)
                return returnlist

            if flag == 1:
                understat = csv.reader(us)
                for row in understat:
                    rows1.append(row)
                z.field_names=rows1[0]
                for i in rows1:
                    if i[3] == name:
                        temp.append(i)
                        if i[0] == '2019':
                            z.add_row(i)
                print("Current Season Player data: ")
                z.sortby = "Goals"
                z.reversesort = True
                print(z)
                pred=predicted_position(rows,name)
                returnlist.append(temp)
            returnlist.append(pred)
            return returnlist

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
    rP=[]
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
            # print(rows4)
            x.field_names=rows4[0]
            y.field_names=rows4[0]
            for i in rows4:
                if i[2] == name:
                    rP.append(i)
                    x.add_row(i)
                    if i[0] == '2019':
                        print(i)
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
                return rP

            #spider chart but doesnt come properly for some reason
            df = pd.DataFrame(dict(
                r=[goals, assists, xG, xA, xG90, xA90],
                theta=['Goals', 'Assists', 'xG',
                       'xA', 'xG90', 'xA90']))
            fig = px.line_polar(df, r='r', theta='theta', line_close=True)
            fig.show()

            return rP


#n = input("Enter: player or team")
#if n=="player":
#    name = input("Enter player name")
#    player(name)
#elif n=="team":
#    name = input("Enter team name")
#    team(name)
#else:
#    print("Invalid input")
#    exit()

@app.route("/api/test", methods=["POST","GET"])
def apiTest():
    a = [1,2,3,4,5];
    b = { 'results': [
    {'a': 1, 'b': 2},
    {'a': 5, 'b': 10}
    ]};
    return jsonify(b);

if __name__ == '__main__':
    app.run(debug=True)
