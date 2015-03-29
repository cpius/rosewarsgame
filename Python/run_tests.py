from tests import utester, setup_tester, controller_tester, speed_tester2


testdict = {
    1:  ("Utester", utester.run),
    2:  ("Setup tester", setup_tester.run),
    3: ("Controller tester", controller_tester.run),
    4: ("Speed Tester", speed_tester2.run)
}


usetests = [3]


if __name__ == '__main__':

    for index in usetests:
        print("---", testdict[index][0], "---")
        testdict[index][1]()
        print()
        print()
