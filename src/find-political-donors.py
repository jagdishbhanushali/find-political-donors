from heapq import heappush as push, heappushpop as pushpop
import datetime
import os
import sys

input_file=sys.argv[1] #"../input/itcont.txt"
zip_output_path=sys.argv[2] #"../output/medianvals_by_zip.txt"
date_output_path=sys.argv[3] #"../output/medianvals_by_date.txt"

class heap_median:
    def __init__(self):
        self.upper = []
        self.lower = []

    def median(self):
        if len(self.upper) > len(self.lower):
            return self.upper[0]
        else:
            return (self.upper[0] - self.lower[0]) / 2.

    def add(self, value):
        value = pushpop(self.upper, value)
        value = -pushpop(self.lower, -value)
        if len(self.upper) <= len(self.lower):
            push(self.upper, value)
        else:
            push(self.lower, -value)

contributers={}

def process(line,consider_other_id=False):
    # all_fields="C00177436|N|M2|P|201702039042410894|15|IND|DEEHAN, WILLIAM N|ALPHARETTA|GA|300047357|UNUM|SVP, SALES, CL|01312017|384||PR2283873845050|1147350||P/R DEDUCTION ($192.00 BI-WEEKLY)|4020820171370029337".strip().split('|')
    all_fields=line.strip().split('|')
    field_index=[0,10,13,14,15] #CMTE_ID,ZIP_CODE,TRANSACTION_DT,TRANSACTION_AMT,OTHER_ID
    fields=[all_fields[i] for i in field_index]

    #Checking CMTEID, TRANSACTION_AMT for non-empty and OTHER_ID for empty
    if(fields[4]=="" and fields[0]!="" and fields[3]!=""):
        # print(fields)
        process_zip(fields)
        process_date(fields)

def process_zip(data):
    contributer=data[0]
    zip_code=data[1][:5]
    amount=float(data[3])

    #Ignoring ZIP length less than 5
    if len(zip_code)< 5:
        return
    #Using dictionary structure to store contributer
    if contributer in contributers :
        if zip_code in contributers[contributer]["ZIP"]:
            total_amount=contributers[contributer]["ZIP"][zip_code]["TOTAL_AMOUNT"]+amount
            count_transaction=contributers[contributer]["ZIP"][zip_code]["COUNT_TRANSACTIONS"]+1
            data=contributers[contributer]["ZIP"][zip_code]["DATA"]
            data.add(amount)
            median=data.median()
            contributers[contributer]["ZIP"][zip_code] = {"TOTAL_AMOUNT": total_amount, "COUNT_TRANSACTIONS": count_transaction, "MEDIAN": median,"DATA":data}
        else:
            total_amount=amount
            data = heap_median()
            data.add(amount)
            median=amount
            count_transaction = 1
            contributers[contributer]["ZIP"][zip_code] = {"TOTAL_AMOUNT": total_amount, "COUNT_TRANSACTIONS": 1, "MEDIAN": median,"DATA":data}
    else:
        total_amount=amount
        data=heap_median()
        data.add(amount)
        median=amount
        count_transaction=1
        contributers[contributer]={"DATE":{},"ZIP":{}}
        contributers[contributer]["ZIP"][zip_code]={"TOTAL_AMOUNT":total_amount,"COUNT_TRANSACTIONS":1,"MEDIAN":median,"DATA":data}
    with open(zip_output_path,"a") as f:
        f.writelines(contributer+"|"+zip_code+"|"+str(round(median))+"|"+str(count_transaction)+"|"+str(round(total_amount))+"\n")

def process_date(data):
    try:
        contributer = data[0]
        #Checking proper date format. ALso works for empty date string
        if(datetime.datetime.strptime(data[2],"%m%d%Y")):
            tr_date = data[2]
        amount = float(data[3])
    except:
        print("Date Exception")
        return

    if contributer in contributers :
        if tr_date in contributers[contributer]["DATE"]:
            total_amount=contributers[contributer]["DATE"][tr_date]["TOTAL_AMOUNT"]+amount
            count_transaction=contributers[contributer]["DATE"][tr_date]["COUNT_TRANSACTIONS"]+1
            data=contributers[contributer]["DATE"][tr_date]["DATA"]
            data.add(amount)
            median=data.median()
            contributers[contributer]["DATE"][tr_date] = {"TOTAL_AMOUNT": total_amount, "COUNT_TRANSACTIONS": count_transaction, "MEDIAN": median,"DATA":data}
        else:
            total_amount=amount
            data = heap_median()
            data.add(amount)
            median=amount
            count_transaction = 1
            contributers[contributer]["DATE"][tr_date] = {"TOTAL_AMOUNT": total_amount, "COUNT_TRANSACTIONS": 1, "MEDIAN": median,"DATA":data}
    else:
        total_amount=amount
        data=heap_median()
        data.add(amount)
        median=amount
        count_transaction=1
        contributers[contributer]={"DATE":{},"ZIP":{}}
        contributers[contributer]["DATE"][tr_date]={"TOTAL_AMOUNT":total_amount,"COUNT_TRANSACTIONS":1,"MEDIAN":median,"DATA":data}

def print_date_contribution():

    with open(date_output_path, "w") as f:
        for contributer in sorted(contributers):
            #Fetching dates converting them to Date type and sorting them
            dates=[datetime.datetime.strptime(d,"%m%d%Y") for d in  contributers[contributer]["DATE"].keys()]
            for d in sorted(dates):
                #Converting back to string type date to fecth from dictionary
                tr_date=d.strftime("%m%d%Y")
                median=contributers[contributer]["DATE"][tr_date]["MEDIAN"]
                count=contributers[contributer]["DATE"][tr_date]["COUNT_TRANSACTIONS"]
                total_amount=contributers[contributer]["DATE"][tr_date]["TOTAL_AMOUNT"]
                f.writelines(contributer+"|"+ tr_date+ "|"+str(round(median)) + "|"+str(count) +"|"+str(round(total_amount))+"\n")


if __name__ == '__main__':
    if(os.path.exists(zip_output_path)):
        os.remove(zip_output_path)
    if (os.path.exists(date_output_path)):
        os.remove(date_output_path)

    with open (input_file) as f:
        for line in f:
            process(line)
            # break
    print_date_contribution()
    # print(contributers)
