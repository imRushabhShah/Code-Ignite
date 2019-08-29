from flask import Flask,request
from googlesearch import search
import os

import bs4

app=Flask(__name__)


@app.route('/',methods=['GET'])
def verify():
    return("ok",200)

@app.route('/testObj',methods=['POST'])
def Testing():
    # args = request.args
    # print(args.keys())
    return {"data":["blablalb","asdasdsd","asdsadsad"],"url":{}}, 200

@app.route('/getErrors',methods=['POST'])
def webhook():
    args = request.args
    # print(args.keys())
    ErrorText = args['ErrorText']
    ClassName = args['ClassName']
    # print(ClassName)
    # print(ErrorText)
    err_code = ExtractErrorfunc(ClassName,ErrorText)
    print("the extracted error message")
    print(err_code)
    print(len(""))
    if err_code=="":
        return ""
    print("going into top hits")
    return top_hits(err_code)
    # return render_template(),200


if __name__=='__main__':
    app.run(debug=True,port=5000)


'''
def ExtractErrorfunc(class_str, err_msg):
    words = class_str.split(' ')

    if words[0] == "<terminated>":
        class_name = words[1]
    else:
        print("Unable to get classname for app: ",app)
    err_lines = err_msg.split("\n\t")
    # print (err_lines)
    # for line in err_lines:

    except_index = err_msg.find('Exception in thread ')
    st_pos = except_index+len('Exception in thread ')
    at_index = err_msg[st_pos:].find('at ')
    # print ("indexes: ",except_index, at_index)
    result = err_msg[st_pos:st_pos + at_index]
    return result

'''


def ExtractErrorfunc(class_str, err_msg):
    if err_msg.startswith("Error: Could not"):
        return err_msg

    if err_msg.find('SIGSEGV') != -1:
        return 'java SIGSEGV'

    # words = class_str.split(' ')
    words = class_str.split(' ')

    class_name = words[1]
    print(class_name)
    print("\n\n\n\n")
    # if words[0] == "<terminated>":
    #     class_name = words[1]
    # else:
    #     print("Unable to get classname for app: ",app)
    err_lines = err_msg.split("\n\t")
    # print (err_lines)
    # for line in err_lines:
    cnt = 0
    except_index = err_msg.find('Exception in thread ')
    st_pos = except_index+len('Exception in thread ')
    at_index = err_msg[st_pos:].find('at ')
    # print ("indexes: ",except_index, at_index)
    dirname1=""
    result = err_msg[st_pos:st_pos + at_index]

    if not os.path.exists(class_name + '_logs'):
        os.mkdir(class_name + '_logs')
        f1 = open(class_name+'_logs'+'/cnt.txt', 'w+')
        f1.write('0')
        f1.close()


    dirname = class_name + '_logs'

    f = open(dirname + '/cnt.txt', 'r')

    cnt = f.read()


    f.close()
    f1 = open(dirname+'/cnt.txt', 'w')
    cnt=int(str(cnt))+1
    if cnt > 11:
        f1.write('0')
    f1.write(str(cnt))
    f1.close()

    f = open(dirname + '/logs.txt', 'a')
    f.write(err_msg)
    f.write('****************')
    dirname1 = dirname
    f.close()

    if cnt >= 10:
        nums = []
        f1 = open(dirname1+'/logs.txt', 'r')
        ans = f1.read()


        f2 = open('report.txt', 'w')

        c = ans.count('java.lang.Error')
        f2.write('\njava.lang.Error occurrences: '+str(c))
        nums.append(c)
        c = ans.count('\njava.lang.ArrayIndexOutOfBoundsException')
        nums.append(c)
        f2.write('\njava.lang.ArrayIndexOutOfBoundsException occurrences: ' + str(c))
        c = ans.count('java.lang.ArithmeticException')
        f2.write('\njava.lang.ArithmeticException occurrences: ' + str(c))
        nums.append(c)

        m = max(nums)
        if nums[0] == m:
            f2.write('\n\nMaximum error types found:'+'java.lang.Error')
        if nums[1] == m:
            f2.write('\n\nMaximum error types found:'+'java.lang.ArrayIndexOutOfBoundsException')
        if nums[2] == m:
            f2.write('\n\nMaximum error types found:'+'java.lang.ArithmeticException')

        f2.close()

    return result

def ret_web_links(err_code):

    top_hits = []

    q = str(err_code) + " " + "site:stackoverflow.com"

    for url in search(q, lang='en', stop=5):
        top_hits.append(url)

    return top_hits


def web_scrapper(tp_links):
    import requests
    import bs4

    parseVal = """"""

    for lk in tp_links:

        res = requests.get(lk)

        if (res.status_code == 200):

            soup_obj = bs4.BeautifulSoup(res.text, 'lxml')

            div_list = soup_obj.findAll('div', attrs={'class': 'js-vote-count'})

            answ_list = soup_obj.findAll('div', attrs={'class': 'post-text'})

            max_votes = 0

            answer_data = """"""

            for i in range(len(div_list)):

                if int(div_list[i]['data-value']) >= max_votes:
                    max_votes = int(div_list[i]['data-value'])

                    answer_data = answ_list[i]

            dt = answer_data.findAll('p')

            for it in dt:
                parseVal += it.text + "\n "

            print(max_votes)

            parseVal += lk + "\n " + 'Upvotes:' + str(max_votes) + '\n'

            parseVal += " __________________________________________________________________" + "\n"

        #   print(parseVal)

    return parseVal

def top_hits(err_code):
    tp_lk = ret_web_links(err_code)

    lng_string = web_scrapper(tp_lk)

    return lng_string