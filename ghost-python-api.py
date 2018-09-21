
import subprocess as sp
import os

class whole:
    def __init__(self):
        # to check whether relex is opened or not
        self.isRelex = False
        # list for storing the user question
        self.all_rule = ""
        # list for storing the user answer
        self.all_answer = []
        # list for storing how many
        self.len_of_output_from_guile = []
        # integer that counts how many times guile was run
        self.running_times = 0
        # file for storing the user question
        self.question_file = open("/home/aman/Questionfile.txt", "a+")

    def takeInput(self):

        # starting the relex server
        if (self.isRelex == False):
            self.startRelex()
            self.isRelex = True

        # starting and cummunicating with the Guile
        self.displayPopen()

        # asking the user continously for what he is looking for
        while (True):
            self.running_times = self.running_times + 1
            value = input("Please enter your rule or '(quit)' to exit: ")
            if (value == "(quit)"):
                found = input("Are you sure? Y or N: ")
                if found == "Y" or found == "y":
                    self.question_file.close()
                    raise SystemExit
                elif found == "N" or found == "n":
                    continue
            # processing the question of user to cummunicate it with Guile
            self.ghostRule(value.encode())

        self.question_file.close()
            # list rule
            # self.listRule()

    def startRelex(self):
        print("-------opening relex server------------")
        # sp.call('./opencog-server.sh', cwd='/home/abeni/relex')
        try:
            os.chdir("/home/aman/relex/")
            os.system("gnome-terminal -e 'bash -c \"./opencog-server.sh; exec bash\"'")
            # sp.call("gnome-terminal --command ='./home/aman/relex/opencog-server.sh'", shell=True)
            # sp.call('sudo docker run -it -p 4444:4444 opencog/relex /bin/sh opencog-server.sh', shell=True)
            print("Relex Server opened successfully")
        except Exception as e:
            print("Error occured in opening relex server", e)

        # if it is using docker
        # subprocess.call('sudo docker run -it -p 4444:4444 opencog/relex /bin/sh opencog-server.sh', shell=True)

    def startRelex2(self):
        a = [1, 2, 3, 4, 5]
        os.chdir("/home/aman/relex/")
        return_code = sp.call("gnome-terminal --command ='./opencog-server.sh'", shell=True)


    def displayPopen(self):
        disp = sp.Popen('guile', stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.STDOUT)
        try:
            a = disp.stdout.readline()
            if ("GNU Guile" in a.decode()):
                if (self.running_times == 0):
                    print("guile successfully opened")
            else:
                print("there is a problem with guile")
        except Exception as e:
            print("Error Occured in starting guile: ", e)

        try:
            mod = ""
            with open('/home/aman/module.txt', 'r') as f:
                for line in f:
                    mod = mod + line
                modtobyte = mod.encode()
                disp.stdin.write(modtobyte)
                if (self.running_times == 0):
                    print("Modules successfully loaded from file")
        except Exception as e:
            print("Error Occured in loading module from file: ", e)

        try:
            code = b"""
					(ghost-parse-file "/home/aman/files.ghost")
					"""
            disp.stdin.write(code)
            if (self.running_times == 0):
                print("data successfully loaded to robot")
                print("you can check by start greeting wz robot (hi robot)")
        except Exception as e:
            print("Error Occured in testing rule: ", e)

        # spliting all the given rule into objects of list
        list_of_rules = self.all_rule.split('\n')
        aa = len(list_of_rules)

        try:
            i = 0
            # its aa-2 because the last elt f[aa-1] is New line('\n') so the last input or current input asked
            # by user is found on f[aa-2]
            while (i <= aa - 2):
                # if the rule is the last rule or the current rule that user expecting its answer
                # to display its answer
                if (i == aa - 2):
                    # extracting the output and error of the current rule asked by user
                    stdou, stder = disp.communicate(input=list_of_rules[aa - 2].encode())

                    # first changing stdou output into string then split it with '\n'
                    self.out = stdou.decode().split('\n')

                    # processing the Guile answer

                    # when you enter a rule and want to display with communicate it didnot display only what you need
                    # it displays all previous output together so how can you avoid this
                    # print(stdou)

                    # so to display only the short breif answer to user by removing the Error and other
                    # bu the problem of this is all the output displayed by every ghost rule is not belongs to only this
                    # five group of categories
                    j = 0
                    current_answer = []
                    while (j < len(self.out)):
                        if ("[INFO] [GHOST] Say:" in self.out[j]) \
                                or ("[WARN] [GHOST]" in self.out[j]) \
                                or ("<unnamed port>" in self.out[j]) \
                                or ("<unspecified>" in self.out[j]) \
                                or ("ERROR: In procedure module-lookup: Unbound variable:" in self.out[j]):
                            # print(self.out[i])
                            current_answer.append(self.out[j])
                        else:
                            pass
                        j = j + 1

                    # now check that whether the output from guile is statement or empty string
                    # because if its empty then displaying empty string to user as guile
                    # if its statement display this statement to user
                    # print("length of self.out", len(self.out))
                    # add the length of the output displayed from guile to length of output from guile
                    self.len_of_output_from_guile.append(len(self.out))
                    # if the output from guile is empty then it is increased by 1 from previous length
                    # but if its not empty its increased by 7, we checked it many times
                    # so append empty string to all answer if output is empty other wise append the output from guile
                    # we go through all this process because if the output from guile is empty it couldnot display this empyt
                    # output to us
                    if ((self.len_of_output_from_guile[len(self.len_of_output_from_guile) - 1] -
                         self.len_of_output_from_guile[
                             len(self.len_of_output_from_guile) - 2]) == 1):
                        self.all_answer.append(" ")
                    else:
                        self.all_answer.append(current_answer[len(current_answer) - 1])

                    # then display the last output to user which is corresponding to the current asked rule
                    print(self.all_answer[len(self.all_answer) - 1])

                # # so from the list of a bunch of output display only the last elt of the list which is most probably
                # # corresponds to the output of the current rule asked by user
                # print("len of list of rules", len(list_of_rules))
                # print(list_of_rules)
                # print("\n")
                #
                # print("len of output", len(current_answer))
                # print(current_answer)
                # print("\n")
                # #print(output[len(output)-1])
                #
                # print("len of all_answer", len(self.all_answer))
                # print(self.all_answer)
                # print("\n")
                # # # print("self.index", self.empty_index)
                # # # print("\n")

                # if the rule is all the previous rule asked by the user
                # this is only just to write
                else:
                    disp.stdin.write(list_of_rules[i].encode())

                i = i + 1
        except Exception as e:
            print("error occured in writing rule", e)

    """
        this is the function that accepts rule from user and communicate it with the process
    """

    def ghostRule(self, rule):
        try:
            # storing all the rule entered by the user to a global variable called all_rule
            ruletostring = rule.decode()
            if ((ruletostring == '')):
                # print("Please enter a rule")
                pass
            else:
                # if(str(rule)[2:3] != "("):
                # 	print("warning: possibly unbound variable: ", str(rule)[2:])
                if (('(ghost-parse-file') in ruletostring
                        or ('(ghost-parse') in ruletostring):
                    self.all_rule = self.all_rule + ruletostring + '\n'
                    self.question_file(ruletostring)
                    self.question_file.write('\n')
                    # with open('/home/aman/userQuestion.txt', 'wb') as file:
                    #     file.write(ruletostring.encode())
                    #     file.write(b'\n')
                    # creating displayPopen method to get the asked result
                    self.displayPopen()
                else:
                    action = '(map cog-name (test-ghost \"{}\"))'.format(ruletostring)
                    self.all_rule = self.all_rule + action + '\n'
                    self.question_file.write(action)
                    self.question_file.write('\n')
                    # with open('/home/aman/userQuestion.txt', 'wb') as file:
                    #     file.write(action.encode())
                    #     file.write(b'\n')
                    # creating displayPopen method to get the asked result
                    self.displayPopen()


        except Exception as e:
            print("Error Occured in writing rule: ", e)

    def listRule(self):
        lisofrule = self.all_rule.split('\n')
        print(len(lisofrule))
        with open('/home/aman/userQuestion.txt', 'wb') as file:
            for rule in lisofrule:
                file.write(rule.encode())
                file.write(b'\n')

print("-------------Welcome-------------")
one = whole()
one.takeInput()
