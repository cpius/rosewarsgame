from tests import utester, setup_tester, controller_tester


testdict = {
    1:  ("Utester", utester.run),
    2:  ("Setup tester", setup_tester.run),
    3: ("Controller tester", controller_tester.run)
}


usetests = [3]


if __name__ == '__main__':

    for index in usetests:
        print("---", testdict[index][0], "---")
        testdict[index][1]()
        print()
        print()
