
# Titanic Data Analysis

## Some Questions to Answer

The dataset includes the fields below :

- passengerId -> the unique identifier of passenger
- Survived -> 1 or 0, survived or not
- Pclass -> Ticket class 1 = 1st, 2 = 2nd, 3 = 3rd
- Name
- Sex
- Age 
- Sibsp -> # of splings or spous on board
- Parch -> # of parents / childer on board
- Ticket -> Ticket Number
- Fare -> Ticket Fare
- Cabin -> the cabin number
- Embraked -> Port of Embarkation	C = Cherbourg, Q = Queenstown, S = Southampton


Based on this fields, below questions may be asked to be answered :

- Was the "Women and Childern first" rule applied on the disaster  ?
- What is the effect of number of family members on a survival rate of a person ?
- Is there any effect of ticket class and fare on the survival ? 




## Preliminery Analysis




```python
import pandas as pd

titanic_data = pd.read_csv("titanic.csv")
titanic_data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35.0</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35.0</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
  </tbody>
</table>
</div>




```python
print titanic_data.shape
titanic_data.describe()
```

    (891, 12)





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Fare</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>714.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>446.000000</td>
      <td>0.383838</td>
      <td>2.308642</td>
      <td>29.699118</td>
      <td>0.523008</td>
      <td>0.381594</td>
      <td>32.204208</td>
    </tr>
    <tr>
      <th>std</th>
      <td>257.353842</td>
      <td>0.486592</td>
      <td>0.836071</td>
      <td>14.526497</td>
      <td>1.102743</td>
      <td>0.806057</td>
      <td>49.693429</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.420000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>223.500000</td>
      <td>0.000000</td>
      <td>2.000000</td>
      <td>20.125000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>7.910400</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>446.000000</td>
      <td>0.000000</td>
      <td>3.000000</td>
      <td>28.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>14.454200</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>668.500000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>38.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>31.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>891.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>80.000000</td>
      <td>8.000000</td>
      <td>6.000000</td>
      <td>512.329200</td>
    </tr>
  </tbody>
</table>
</div>



As seen above, titanic data has 891 rows however age fields of 177 rows are missing.

So that, firstly the NaN values need to be filled or those rows can be removed. Instead of removing the rows, I prefer to fill those missing values.

In order to fill the missing values, mean or median of age field can be used. In this case I prefer to use median.



```python
age_median = titanic_data['Age'].median()
titanic_data['Age'] = titanic_data['Age'].fillna(age_median) 
titanic_data.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Fare</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
      <td>891.000000</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>446.000000</td>
      <td>0.383838</td>
      <td>2.308642</td>
      <td>29.361582</td>
      <td>0.523008</td>
      <td>0.381594</td>
      <td>32.204208</td>
    </tr>
    <tr>
      <th>std</th>
      <td>257.353842</td>
      <td>0.486592</td>
      <td>0.836071</td>
      <td>13.019697</td>
      <td>1.102743</td>
      <td>0.806057</td>
      <td>49.693429</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>1.000000</td>
      <td>0.420000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>223.500000</td>
      <td>0.000000</td>
      <td>2.000000</td>
      <td>22.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>7.910400</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>446.000000</td>
      <td>0.000000</td>
      <td>3.000000</td>
      <td>28.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>14.454200</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>668.500000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>35.000000</td>
      <td>1.000000</td>
      <td>0.000000</td>
      <td>31.000000</td>
    </tr>
    <tr>
      <th>max</th>
      <td>891.000000</td>
      <td>1.000000</td>
      <td>3.000000</td>
      <td>80.000000</td>
      <td>8.000000</td>
      <td>6.000000</td>
      <td>512.329200</td>
    </tr>
  </tbody>
</table>
</div>



#### Checking Other Mising Values

Lets check for other missing values.



```python
titanic_data.isnull().sum()
```




    PassengerId      0
    Survived         0
    Pclass           0
    Name             0
    Sex              0
    Age              0
    SibSp            0
    Parch            0
    Ticket           0
    Fare             0
    Cabin          687
    Embarked         2
    dtype: int64



So that, Cabin and Embarked fields still have missing values. Lets fill those fields.
Cabin field is a categorical data, so it is going to be filled with "UNKNOWN".


```python
titanic_data["Cabin"] = titanic_data["Cabin"].fillna("UNKNOWN")
titanic_data.isnull().sum()
```




    PassengerId    0
    Survived       0
    Pclass         0
    Name           0
    Sex            0
    Age            0
    SibSp          0
    Parch          0
    Ticket         0
    Fare           0
    Cabin          0
    Embarked       2
    dtype: int64



Now lets fill Embarked field.


```python
titanic_data.groupby("Embarked").count()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
    </tr>
    <tr>
      <th>Embarked</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>C</th>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
      <td>168</td>
    </tr>
    <tr>
      <th>Q</th>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
      <td>77</td>
    </tr>
    <tr>
      <th>S</th>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
      <td>644</td>
    </tr>
  </tbody>
</table>
</div>



Embarked field has C, Q, and S. So missing values are filled with "U" indicating unknown.



```python
titanic_data["Embarked"] = titanic_data["Embarked"].fillna("U")
titanic_data.isnull().sum()
```




    PassengerId    0
    Survived       0
    Pclass         0
    Name           0
    Sex            0
    Age            0
    SibSp          0
    Parch          0
    Ticket         0
    Fare           0
    Cabin          0
    Embarked       0
    dtype: int64



Now the missing values are filled. The operations on age field will continue on the next sections.

## Analysis On Fields


### Sex



```python
import matplotlib.pyplot as plt
%matplotlib inline

# Sex distribution based on survival rate
survived_sex = titanic_data[titanic_data['Survived']==1]['Sex'].value_counts()
not_survived_sex = titanic_data[titanic_data['Survived']==0]['Sex'].value_counts()

# This function will be used multiple times.
# NEw plotting is changed 
def plot_survival_rate_by_field(field_name):
    gb = titanic_data.groupby(field_name)['Survived'].mean()*100
    plot = gb.plot(kind='bar', title="Titanic Passengers Survival Rate by " + field_name)
    plot.set_xlabel(field_name)
    plot.set_ylabel("Survival Rate in %")
    
    
    
plot_survival_rate_by_field("Sex")
```


![png](output_16_0.png)


As seen in plots above, The survival rate of women is higher than man. There seems a correlation between the gender and survival rate. 

### Age

For analyzing age, an new field is created by categorizing ages into groups such as infant, child, youth, adult and old. 


Please Refer to : http://www.widener.edu/about/campus_resources/wolfgram_library/documents/life_span_chart_final.pdf


```python
# NEW : Age Group Generation
max_age = titanic_data['Age'].max()
age_labels = ["INFANT", "CHILD", "YOUTH", "ADULT", "MIDDLEAGE", "OLD"]    
titanic_data['AgeGroup'] = pd.cut(titanic_data['Age'],
                                  [0, 2, 12, 25, 40, 60, max_age],
                                  labels=age_labels)
titanic_data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
      <th>AgeGroup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>YOUTH</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
      <td>ADULT</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35.0</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
      <td>ADULT</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35.0</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
    </tr>
  </tbody>
</table>
</div>



Now all ages were categorized into groups. Lets visualize the relation between age groups and survival. In order to see properly, the data needs to be normalized based on the distribution of age groups in the whole data.

In order to find the survival ratio, for each age group the number of survivors are divided by the number of attendees.



```python
# Age Group distribution based on survival rate
plot_survival_rate_by_field("AgeGroup")

```


![png](output_21_0.png)


The youngers survival rate is higher than the olders based on the plot above. So that, age is effective on survival.

> __Was the "Women and Childern first" rule applied on the disaster ?__
Based on the analysis on Sex and Age fields, women and younger people survived more in the disaster.



### Family Members

In order to analyze the effect of number of family members to survival rate, a new field will be created as FamMem which is simply the sum of SibSp and Parch fields. This fields show that the number of family members on board.


```python
titanic_data['NumberOfFamilyMembers'] = titanic_data['SibSp'] + titanic_data['Parch']

def fam_group(femSize):
    if femSize == 0:
        return "SINGLE"
    elif femSize > 0 and femSize < 5:
        return "SMALLFAMILY"
    elif femSize > 5:
        return "LARGEFAMILY"
    
    
titanic_data['GroupByFamilySize'] = titanic_data['NumberOfFamilyMembers'].apply(fam_group)
titanic_data.head()

```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
      <th>AgeGroup</th>
      <th>NumberOfFamilyMembers</th>
      <th>GroupByFamilySize</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>YOUTH</td>
      <td>1</td>
      <td>SMALLFAMILY</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
      <td>ADULT</td>
      <td>1</td>
      <td>SMALLFAMILY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
      <td>0</td>
      <td>SINGLE</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35.0</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
      <td>ADULT</td>
      <td>1</td>
      <td>SMALLFAMILY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35.0</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
      <td>0</td>
      <td>SINGLE</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Normalization
plot_survival_rate_by_field("GroupByFamilySize")
```


![png](output_26_0.png)




> __What is the effect of number of family members on a survival rate of a person ?__
Based on the family size of the passengers, the passengers who have a large family are less likely to survive comparing to singles and small families.

### Fare & Ticket Class

In order to investigate whether the wealth is effective on survival in the disaster, ticket fares and ticket class are need to by analyzed. First of all, in order to see the correlation of these two fields the histogram is drawn.


```python
## 1st, 2nd, 3rd
plot_survival_rate_by_field("Pclass")

```


![png](output_29_0.png)



```python
titanic_data["Fare"].describe()
```




    count    891.000000
    mean      32.204208
    std       49.693429
    min        0.000000
    25%        7.910400
    50%       14.454200
    75%       31.000000
    max      512.329200
    Name: Fare, dtype: float64



So Fare changes between 0 - 512.3292. The cut points might be 0 - 50, 50 - 200 and 200 - max_value.
I have selected cut values using the histogram below.


```python
titanic_data["Fare"].hist()
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7fc04bcb6990>




![png](output_32_1.png)



```python
fare_labels = ["LOW", "MID", "HIGH"] 
max_fare = titanic_data['Fare'].max()
titanic_data['FareGroup'] = pd.cut(titanic_data['Fare'],
                                  [0, 50, 200, max_fare],
                                  labels=fare_labels)
titanic_data.head()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
      <th>AgeGroup</th>
      <th>FemMem</th>
      <th>FemGroup</th>
      <th>FareGroup</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>YOUTH</td>
      <td>1</td>
      <td>SMALLFEM</td>
      <td>LOW</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
      <td>ADULT</td>
      <td>1</td>
      <td>SMALLFEM</td>
      <td>MID</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
      <td>0</td>
      <td>SINGLE</td>
      <td>LOW</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35.0</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
      <td>ADULT</td>
      <td>1</td>
      <td>SMALLFEM</td>
      <td>MID</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35.0</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>UNKNOWN</td>
      <td>S</td>
      <td>ADULT</td>
      <td>0</td>
      <td>SINGLE</td>
      <td>LOW</td>
    </tr>
  </tbody>
</table>
</div>




```python
plot_survival_rate_by_field("FareGroup")
```


![png](output_34_0.png)


So it is seen that, survival rate of lover class passengers is less then the higher class passengers according to ticket fares and classes.

Passengers who has lower fare tickets seems to be dead more likely. The reason might be rescuing the passengers with higher fare tickets before the lower ones.

> __- Is there any effect of ticket class and fare on the survival ? __ Ticket fares and class of passengers are seemed to be correlated with survival rate based on the analysis. Higher class passengers were less likely to be dead. 

### One More Analysis

The correlation of fields in the data can also be found using pandas built-in functions.


```python

titanic_data.corr()['Survived'].abs().sort_values()

```




    PassengerId    0.005007
    FemMem         0.016639
    SibSp          0.035322
    Age            0.064910
    Parch          0.081629
    Fare           0.257307
    Pclass         0.338481
    Survived       1.000000
    Name: Survived, dtype: float64



As seen in the correlations above, SexN, Pclass, Fare, AgeGroupN are most correlated with survived field.

## Conclusion

There are 3 questions I have asked based on the data.

>- Was the "Women and Childern first" rule applied on the disaster  ?
- What is the effect of number of family members on a survival rate of a person ?
- Is there any effect of ticket class and fare on the survival ? 

Based on the analysis, 

- Women and children in titanic survived more, however the age of some passengers were missing and filled with median of all ages.
- Persons who have large families are survived less based on the data provided. 
- Lower class passengers survived less.

All the analysis above are done by filling some missing values and the provided data set is a small subset of passengers. Please read this report considering those limitations.







## References


http://pandas.pydata.org/pandas-docs/stable/
