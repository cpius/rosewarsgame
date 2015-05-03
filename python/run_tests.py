from tests import utester, setup_tester, controller_tester, speed_tester, ai_tester

testdict = {
    1:  ("Utester V 1.0", utester.run10),
    2:  ("Utester V 1.1", utester.run11),
    3:  ("Setup tester", setup_tester.run),
    4: ("Controller tester", controller_tester.run),
    5: ("Speed tester", speed_tester.test_action_getter),
    6: ("AI tester", ai_tester.run)
}

usetests = [2]

if __name__ == '__main__':

    for index in usetests:
        print("---", testdict[index][0], "---")
        testdict[index][1]()
        print()
        print()
