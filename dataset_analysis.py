from collections import Counter
from numpy import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)

# class Person with attributes Age,Gender,State,Phone_number,Height,Weight


class Person:
    def __init__(self, age, gender, state, phone_num, height, weight):
        self.Age = age
        self.Gender = gender
        self.State = state
        self.Phone_number = phone_num
        self.Height = height
        self.Weight = weight

# Used for generating classes from the data read from dataset.txt
# Reads data from data.txt and creates a class for each line in the file with the data as it's attributes


def loading_class():
    fp = open("dataset.txt", "r")
    temp = []
    for x in fp:
        y = x.split(",")
        temp.append(Person(int(y[0]), y[1], y[2],
                    int(y[3]), float(y[4]), float(y[5])))
    return temp

# calculates average height of all the People and returns it


def cal_avg_height(ls):
    sum = 0
    for obj in ls:
        sum += obj.Height
    return sum/(len(ls))

# calculates average weight of all the People and returns it


def cal_avg_weight(ls):
    sum = 0
    for obj in ls:
        sum += obj.Weight
    return sum/len(ls)


# main function
if __name__ == "__main__":
    # list of 28 states
    states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh",
              "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
    # creates 10000 sized array of states where each element is randomly selected
    state = np.asarray(random.choice(states, 10000))
    # 10000 sized array of different age vales uniformly distributed between [1,100]
    age = np.random.randint(1, 100, (10000,))
    sex = ["Male", "Female"]
    # randomly selecting gender for all 10000 classes
    gender = np.asarray(random.choice(sex, 10000))
    # selecting phone number randomly with starting digits 6,7,8,9
    phone_num = np.random.randint(
        6000000000, 9999999999, (10000,), dtype=np.int64)
    # selecting 10000 values for height of Person from guassian distribution with mean 160cm and deviation 10cm
    height = np.random.normal(loc=160, scale=10, size=(10000,))
    # selecting 10000 values for weight of Person from guassian distribution with mean 70kg and deviation 5kg
    weight = random.normal(loc=70, scale=5, size=(10000,))

    # Creating dataset.txt with random data selected above
    fp = open("dataset.txt", "w")
    fp.close()
    fp = open("dataset.txt", "a")
    for i in range(10000):
        fp.write("%d,%s,%s,%d,%f,%f" % (
            age[i], gender[i], state[i], phone_num[i], height[i], weight[i]))
        if i != 9999:
            fp.write("\n")
    fp.close()

    # Creating 10000 instances of class Person
    obj_ls = loading_class()
    avg_height = cal_avg_height(obj_ls)
    avg_weight = cal_avg_weight(obj_ls)

    # appending average weights and heights of all 10000 instances in dataset.txt
    fp = open("dataset.txt", "a")
    fp.write("\n%d\n%d" % (avg_height, avg_weight))
    fp.close()

    male = []
    female = []
    male_age = []
    female_age = []
    for obj in obj_ls:
        if obj.Gender == "Male":
            male.append(obj)
            male_age.append(obj.Age)
        else:
            female.append(obj)
            female_age.append(obj.Age)

    gend_count = [len(male), len(female)]
    phnum_count = [0, 0, 0, 0]
    for x in obj_ls:
        if x.Phone_number >= 6000000000 and x.Phone_number < 7000000000:
            phnum_count[0] += 1
        elif x.Phone_number >= 7000000000 and x.Phone_number < 8000000000:
            phnum_count[1] += 1
        elif x.Phone_number >= 8000000000 and x.Phone_number < 9000000000:
            phnum_count[2] += 1
        else:
            phnum_count[3] += 1

    # saving the respective height plots in height.jpg
    plt.figure()
    fig, axs = plt.subplots(ncols=2)
    p1 = sns.histplot(x=[x.Height for x in male], kde=True, ax=axs[0])
    p2 = sns.histplot(x=[x.Height for x in female], kde=True, ax=axs[1])
    p1.set(xlabel='Height (in cm)', ylabel="Number of Males")
    p2.set(xlabel="Height (in cm)", ylabel="Number of Females")
    plt.tight_layout()
    plt.savefig("height.jpg")

    # saving respective weight plots in weight.jpg
    plt.figure()
    fig, axs = plt.subplots(ncols=2)
    p1 = sns.histplot(x=[x.Weight for x in male], kde=True, ax=axs[0])
    p2 = sns.histplot(x=[x.Weight for x in female], kde=True, ax=axs[1])
    p1.set(xlabel="Weight (in kg)", ylabel="Number of Males")
    p2.set(xlabel="Weight (in kg)", ylabel="Number of Females")
    plt.tight_layout()
    plt.savefig("weight.jpg")

    # saving pie chart of genders in gender.jpg
    plt.figure()
    plt.pie(gend_count, labels=["Male", "Female"],
            autopct="%.2f%%", shadow=True)
    plt.savefig("gender.jpg")

    # saving pie chart phone numbers starting digit in phone.jpg
    plt.figure()
    plt.pie(phnum_count, labels=["6", "7", "8", "9"],
            autopct="%.2f%%", shadow=True)
    plt.savefig("phone.jpg")

    # saving line plots of cdf of age vs age in age.jpg
    plt.figure()
    plt.plot(list(Counter(sorted(male_age)).keys()), np.cumsum(
        np.array(list(Counter(sorted(male_age)).values()))), label="Male")
    plt.plot(list(Counter(sorted(female_age)).keys()), np.cumsum(
        np.array(list(Counter(sorted(female_age)).values()))), label="Female")
    plt.xlabel("Age")
    plt.ylabel("Frequency of people below certain age")
    plt.legend(title="cdf of age of male and female", loc="best")
    plt.savefig("age.jpg")

    # saving number of people in each state as a bar plot in state.jpg
    plt.figure()
    plt.bar(list(Counter(sorted(state)).keys()),
            list(Counter(sorted(state)).values()))
    plt.xticks(list(Counter(sorted(state)).keys()), list(
        Counter(sorted(state)).keys()), rotation="vertical")
    plt.ylabel("Number of people")
    plt.xlabel("States")
    plt.savefig("state.jpg", bbox_inches="tight")
