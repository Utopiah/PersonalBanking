# Personal Banking, module to read a bank statement in CSV format and show patterns

import pandas as pd
#import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
import datetime as dt
from datetime import datetime

COLUMNNAMES = (
    'AccountNumber',     # not useful, always the same
    'AccountName',         # idem
    'TargetAccount',    # useful only for transfers
    'ID',            # unique ID
    'DateAccounting',    # date of registration
    'Date',            # date of purchase
    'Amount',        # negative value for spending money, positive for receiving (switched)
    'Currency',        # seems to be always EUR
    'Label',        # details of the transaction, useful for grouping
    'Details',
    'Message'
    )
bankmovements = pd.read_csv('x', ';', COLUMNNAMES, header=0)
#dtype={'Amount':float},

bankmovements = bankmovements.dropna(subset=['Date'])
#drops special movements e.g. message for receivng new card
totalmovements = len(bankmovements.index)

for i in bankmovements.index[1:]:
    bankmovements['Amount'][i] = -float(str(bankmovements['Amount'][i]).replace(',', '.'))
    #could use locale instead but requires to work on the target computer
    bankmovements['Date'][i] = datetime.strptime(str(bankmovements['Date'][i]), '%d/%m/%Y')
bm = bankmovements.ix[1:]

print "-TOTAL-------------------------------------------------"
print "Starting range: ", min(bm['Date'])
print "Ending range: ", max(bm['Date'])
print "Total number of movements: ", totalmovements
print "Mean: ", round(bm['Amount'].abs().mean(), 2)
print "Sum: ", bm['Amount'].sum()
print "Absolute sum: ", bm['Amount'].abs().sum()
print "Min: ", bm['Amount'].min()
print "Max: ", bm['Amount'].max()

#TODO use to slice by month
targetmonthindices = []
for i in bankmovements.index[1:]:
    if (bm['Date'][i].year == 2014) & (bm['Date'][i].month == 9):
    #example of September 2014
        targetmonthindices.append(i)

targetindices = bm.index
targetindices = targetmonthindices

#TODO fail maybe because of rounding
#print bm['Amount'][bm['Amount'].min()]

salaries = ['AGROPROMOTION', 'CARGILL']
#in Details not Label
#warning, salaries is in income so negative here

food = ['PANOS', 'DELH', 'CARREF', 'GB EXPR']
housecare = ['WIBRA', 'HEMA']
services = ['LAMPIRIS', 'BELGACOM']
transports = ['SNCB', 'STIB']
travel = ['AIRLINE']
rent = ['Aziz', 'rent']
cash = ['ithdrawal']

groups = [food, services, transports, rent, cash, travel, housecare]

incomeindices=[]
print "-INCOMES-------------------------------------------------"
for i in targetindices:
    if bm['Amount'][i] < 0:
        #print bm['Details'][i]
        incomeindices.append(i)
print "Sum of incomes: ", bm['Amount'][incomeindices].sum()
#dropping those indices from targetindices
#print targetindices
print len(targetindices)
#print incomeindices
print len(incomeindices)
targetindices = set(targetindices) - set(incomeindices)
print len(targetindices)

print "-EXPENSES-------------------------------------------------"
total = bm['Amount'][targetindices].sum()
print "Total: ", total

#TODO add to a table in order to facilitate plotting and comparison
print "-GROUPS-------------------------------------------------"
eventsindexes = []
props = []
for group in groups:
    grpindexes = []
    print "Group: ", group
    for pattern in group:
        for i in targetindices:
            if (pattern in str(bm['Label'][i])) or (pattern in str(bm['Details'][i])):
                eventsindexes.append(i)
                grpindexes.append(i)
    propgrp = 0
    if grpindexes:
        print "Sum: ", bm['Amount'][grpindexes].sum()
        propgrp = round((bm['Amount'][grpindexes].sum()/total)*100, 2)
        print "Proportion: ", propgrp, "%"
        print "Mean: ", round(bm['Amount'][grpindexes].mean(), 2)
        print "Max: ", bm['Amount'][grpindexes].max()
        print "Min: ", bm['Amount'][grpindexes].min()
    props.append(propgrp)
    print "Number of events found: ", len(grpindexes)
props.append(100-sum(props))
                
print "-EVENTS FOUNDS-------------------------------------------------"
print "Number of events found: ", len(eventsindexes)
print "Number of events still to classify: ", totalmovements-len(eventsindexes)
print "Total number of movements: ", totalmovements
print "-EVENTS TO GROUP-------------------------------------------------"
for i in (bm.index-eventsindexes)[:10]:
    print bm['Label'][i]

plt.figure()
plt.plot(bm['Amount'][:])
plt.savefig('myAccounting.png')

plt.figure()
#labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
#sizes = [15, 30, 45, 10]
#colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
#explode = (0, 0.1, 0, 0) # only "explode" the 2nd slice (i.e. 'Hogs')
groups.append('Misc')
labels=groups
sizes=props
print labels
print sizes

plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.savefig('myAccountingByGroups.png')
