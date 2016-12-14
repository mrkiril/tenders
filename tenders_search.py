print("tenders_search")
import sys
import os
import requests
import re
import json
import numpy as np
import math
import operator
import matplotlib
import pylab
import matplotlib.pyplot as plt
from pylab import *
from collections import OrderedDict
# with open('files/files/'+arr_folders1[j], 'w') as f1:
#            f1.write(r2.text)


class Myerror(Exception):
    pass


class Support(object):
    """docstring for ClassName"""

    def pirson(self, a, b):
        while len(a) < len(b):
            a.append(a[-1])

        while len(b) < len(a):
            b.append(b[-1])

        if len(set(a)) == 1 and a[0] != 1:
            for i in range(len(a)):
                a[i] = a[i] - 0.00000001 * i

        if len(set(b)) == 1 and b[0] != 1:
            for i in range(len(b)):
                b[i] = b[i] - 0.00000001 * i

        mean_a = np.mean(a)
        mean_b = np.mean(b)
        sum_1 = 0.0
        for i in range(len(a)):
            sum_1 += (a[i] - mean_a) * (b[i] - mean_b)

        sum_2 = 0.0
        sum_3 = 0.0

        for i in range(len(a)):
            sum_2 += (a[i] - mean_a)**2
            sum_3 += (b[i] - mean_b)**2

        sum_4 = math.sqrt(sum_2 * sum_3)
        return sum_1 / sum_4

    def to_winners(self, folders):
        win_list = {}
        winners_list = os.listdir(folders)
        ii = 0
        for el in winners_list:
            sys.stdout.flush()
            sys.stdout.write("\r%.1f%%" % (ii * 100 / len(winners_list)))
            ii += 1
            tmp_tend_numb = None
            tmp_tel = None
            tmp_email = None
            tmp_edrpou = None
            tmp_corelation = None
            tmp_points = {}
            # table_edrpou - таблиця співвідношення між едрпоу і кодом в
            # тендері
            table_edrpou = {}
            tmp_path = os.path.abspath(el)

            # print(tmp_path)
            #_=input()
            with open(folders + "/" + el, "r") as f:
                pars = json.loads(f.read())

            # Create table
            try:
                for el_1 in pars["timeline"]["results"]["bids"]:
                    try:
                        table_edrpou[el_1["bidder"]] = str(
                            el_1["identification"][0]["identifier"]["id"])
                    except KeyError as e:
                        table_edrpou[el_1["bidder"]] = "None"

            except TypeError as ex:
                continue
            #_ = input()
            # Push initial element
            for el in pars["timeline"]["auction_start"]["initial_bids"]:
                tmp_points[el["bidder"]] = [el["amount"]]

            # Push other element
            for i in range(1, 4):
                for el in pars["timeline"]["round_" + str(i)]:
                    try:
                        elem = pars["timeline"]["round_" + str(i)][el]
                        if "amount" in pars["timeline"]["round_" + str(i)][el]:
                            tmp_points[elem["bidder"]].append(
                                int(elem["amount"]))

                        else:
                            tmp_points[elem["bidder"]].append(
                                tmp_points[elem["bidder"]][-1])
                    except KeyError as exc:
                        continue

            first_in = True
            min_id = ""
            amount = 0
            text = ""
            for el in pars["timeline"]["results"]["bids"]:
                if first_in:
                    min_id = el["bidder"]
                    amount = int(el["amount"])
                    first_in = False
                    text = el

                if int(el["amount"]) < int(amount):
                    amount = int(el["amount"])
                    min_id = el["bidder"]
                    text = el

            tmp_tend_numb = pars["id"]
            tmp_edrpou = table_edrpou[str(min_id)]
            tmp_participants = []

            for elems in pars["timeline"]["results"]["bids"]:
                try:
                    tmp_participants.append(elems["identification"][
                        0]["identifier"]["id"])
                    # print("Lal")
                except Exception as e:
                        # print(elems)
                        #_=input()
                        #print("Loluchka\r\nWTF Error @&*^% ???")
                    continue

            try:
                tmp_tel = text["identification"][
                    0]["contactPoint"]["telephone"]
                tmp_email = text["identification"][0]["contactPoint"]["email"]
            except KeyError as e:
                mp_tel = "None"
                tmp_email = "None"

            try:
                pirson_list = []
                for el in tmp_points.keys():
                    if el != min_id:
                        p_coef = self.intersection(
                            tmp_points[min_id], tmp_points[el])
                        pirson_list.append(p_coef)

                if np.mean(pirson_list) == 0:
                    tmp_corelation = (np.mean(pirson_list)) * \
                        self.slope(tmp_points[min_id])

                elif np.mean(pirson_list) != 0:
                    tmp_corelation = (1 / np.mean(pirson_list)) * \
                        self.slope(tmp_points[min_id])

                tmp_points = tmp_points[min_id]

            except Myerror as e:
                print(tmp_path)
                _ = input("Myerror BRPOINT")

            except TypeError as e:
                print(e)
                print(pirson_list)
                _ = input("Break point")

            win_list[tmp_tend_numb] = Winners(
                tel=tmp_tel,
                email=tmp_email,
                edrpou=tmp_edrpou,
                corelation=tmp_corelation,
                points=tmp_points,
                participants=tmp_participants,
                tender_number=pars["tenderId"],
                tender_id=tmp_tend_numb,
                path=tmp_path
            )
        return win_list

    def slope(self, y1):
        y = np.array(y1)
        x = np.array([0.0, 1.0, 2.0, 3.0])
        z = np.polyfit(x, y, 1)
        if(z[0] == 0):
            z[0] = 0.000001
        #print("z1: ", z[1])
        #print("z0: ", z[0])
        return abs(z[1] / z[0])

    def intersection(self, a, b):
        while len(a) < len(b):
            # print(a)
            # print(b)
            #raise Myerror
            #_=input("intersection break point")
            a.append(a[-1])

        while len(b) < len(a):
            # print(a)
            # print(b)
            #raise Myerror
            #_=input("intersection break point")
            b.append(b[-1])

        if a[0] > b[0] and a[-1] > b[-1]:
            return 0

        elif a[0] > b[0] and a[-1] < b[-1]:
            return 1

        elif a[0] < b[0] and a[-1] < b[-1]:
            return 0

        elif a[0] < b[0] and a[-1] > b[-1]:
            return 1

        else:
            return 0

    def to_customers(self, folders):
        custom_return_list = []
        customers_list = os.listdir(folders)
        ii = 0
        for el in customers_list:
            tmp_edrpou = None
            sys.stdout.flush()
            sys.stdout.write("\r%.1f%%" % (ii * 100 / len(customers_list)))
            ii += 1

            with open(folders + "/" + el, "r") as f:
                pars = json.loads(f.read())

            tmp_id = pars["id"]
            tmp_edrpou = pars["procuringEntity"]["identifier"]["id"]
            custom_return_list.append(Customers(
                edrpou=tmp_edrpou,
                id=tmp_id,
                tender_number=pars["tenderID"],
                tender_id=pars["id"]
            ))
        return custom_return_list

    def cust_connections(self, cust_list, win_list):
        cust_dick = {}
        cust_was = []
        for i in range(len(cust_list)):
            sys.stdout.flush()
            sys.stdout.write("\r%.1f%%" % (i * 100 / len(cust_list)))

            for j in range(i, len(cust_list)):

                if cust_list[i].edrpou == cust_list[j].edrpou and cust_list[i].edrpou not in cust_was:
                    if cust_list[j].edrpou in cust_dick:
                        cust_dick[cust_list[j].edrpou].append(
                            cust_list[j].tender_id)

                    else:
                        cust_dick[cust_list[i].edrpou] = [
                            cust_list[i].tender_id]

            # print(cust_dick)
            #_=input()
            cust_was.append(cust_list[i].edrpou)
        return cust_dick

    def bad_boy_finder(self, cust_list):
        resp_cust = {}
        resp_part = {}
        ii = 0
        for key, val in cust_list.items():
            sys.stdout.flush()
            sys.stdout.write("\r%.1f%%" % (ii * 100.0 / len(cust_list)))
            ii += 1
            
            num_corelations = []
            for win in val:
                try:
                    try:
                        c_ex = winners_list[win]
                        num_corelations.append(c_ex.corelation)                        
                    except KeyError as e:
                        continue

                    if c_ex.edrpou != "None":
                        if c_ex.edrpou in resp_part:
                            #print("in resp part")
                            tmp_index = resp_part[c_ex.edrpou]["index"]
                            tmp_count = resp_part[c_ex.edrpou]["count"]
                            tmp_base = resp_part[c_ex.edrpou]["base"]
                            if type(tmp_base) != list:
                                print(resp_part[c_ex.edrpou])
                                _ = input()

                            resp_part[c_ex.edrpou] = {"count": tmp_count + 1,
                                                      "index": tmp_index + c_ex.corelation,
                                                      "base": tmp_base.append({"index": c_ex.corelation, "path": c_ex.path})
                                                      }
                            print( resp_part[c_ex.edrpou] )
                            _=input("bla bla bla ...")
                        else:
                            print("\r\n First in\r\n")
                            resp_part[c_ex.edrpou] = {
                                                        "count": 1,
                                                        "index": c_ex.corelation,
                                                        "base": [{"index": c_ex.corelation,
                                                                  "path": c_ex.path}]
                                                    }
                            
                except KeyError as e:
                    print(e)
                    _=input("Some Key ERROR")
                    continue

            # середній індекс конкуренції у цього замовника
            if num_corelations != []:
                resp_cust[key] = np.mean(num_corelations)
        
        print("LOLUSHKA")
        _=input()
        #d_descending = OrderedDict(sorted(num_part.items(), key=lambda kv: kv[1]['key3'], reverse=True))
        # base for avarage index for all partisipants
        new_resp_part = {}
        for key, val in resp_part.items():
            new_resp_part[key] = {
                                    "average_index": val["index"] / val["count"], 
                                    "base": val["base"]
                                }

        new_new_resp_part = sorted(new_resp_part.items(), key=lambda kv: kv[
                                   1]['average_index'], reverse=True)

        new_custom = sorted(resp_cust.items(),
                            key=lambda kv: kv[1], reverse=True)

        print(new_custom)
        _ = input("Break Point ...")
        return(new_new_resp_part, new_custom)


class Winners(object):
    """docstring for Winners"""

    def __init__(self, tel, email, edrpou, corelation, tender_number, points, participants, tender_id, path):
        self.tel = tel
        self.email = email
        self.edrpou = edrpou
        self.corelation = corelation
        self.tender_number = tender_number
        self.points = points
        self.participants = participants
        self.tender_id = tender_id
        self.path = path


class Customers(object):
    """docstring for Customers"""

    def __init__(self, edrpou, id, tender_number, tender_id):
        self.edrpou = edrpou
        self.id = id
        self.tender_number = tender_number
        self.tender_id = tender_id

supp = Support()
winners_list = supp.to_winners("points")
print("\r\nwin")
# for v in winners_list.values():
#    print("%.5f" %  (v.corelation) )


customers_list = supp.to_customers("files")
print("\r\nwin win")
new_customers = supp.cust_connections(customers_list, winners_list)
print("\r\nwin win win")
part, custom = supp.bad_boy_finder(new_customers)
print("\r\nwin win win win")

#d_descending = OrderedDict(sorted(bad_customers.items(), key=lambda kv: kv[1]['pirs']))
# for k, v in d_descending.items():
#    #print(k, round(float(v["pirs"]),3 ), round(float(v["aver"]),3 ))
#    print ('%s \t %.4f \t %.4f' % ( k, (v["pirs"]) , v["aver"] ))

'''
with open("xustomers", "wt") as f:
    for i in  range(len(d_descending)):
        k = d_descending[i][0]
        v = d_descending[i][1]
        f.write(  'EDRPOU: %s \t items %.4f \t count %.4f' % ( k, v["items"] , v["count"] )  )
        f.write("\r\n")
'''
with open("customers", "wt") as f:
    for i in range(len(custom)):
        f.write('EDRPOU: %s \t items %.4f \t count %.4f' %
                (k, v["items"], v["count"]))
        f.write("\r\n")
